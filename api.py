import ast
import pandas as pd
from flask import Flask, jsonify  # request
from flasgger import Swagger
from flasgger.utils import swag_from

from resources import constants


SWAGGER_CONFIG = {
    "headers": [
    ],
    "specs": [
        {
            "version": "0.1",
            "title": "Humanitarian Data Service",
            "description": "Consolidating fragmented raw sources of humanitarian data and serving up parsed and "
                           "cleaned data from a single API",
            "endpoint": 'spec',
            "route": '/spec',
            "rule_filter": lambda rule: True  # all in
        }
    ],
    "static_url_path": "/apidocs",
    "static_folder": "swaggerui",
    "specs_route": "/specs"
}

app = Flask(__name__)
api = Swagger(app, config=SWAGGER_CONFIG)


@app.route('/')
def hello():
    # background: https://uigradients.com/#GrapefruitSunset
    landing_page = """
      <!DOCTYPE html>
      <html>
      <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style type="text/css">
        body {
            padding: 50px 200px;
            font-family: "Georgia";
            color: #EEEEEE;
            text-align: center;
            background: linear-gradient(to left, #E96443 , #904E95);
        }
        </style>
      </head>
      <body>
        <h1> Welcome to the Humanitarian Data Service</h1>
        <i class="fa fa-globe" style="font-size:48px;"></i>
        <p>See the interactive API docs <a href="/apidocs/index.html" style="color: #EEEEEE">here</a> </p>
        <p>See the open source repository <a href="https://github.com/dragonaire/humdata" style="color: #EEEEEE">here</a></p>
      </body>
      </html>
    """
    return landing_page


@app.route('/funding/totals/<string:country>/', methods=['GET'])
@swag_from('api_configs/funding_totals_by_country.yml')
def get_funding_totals(country):
    country = country.strip().capitalize()
    funding_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'hno_funding_2016_2017.csv']), encoding='utf-8')
    funding_df = funding_df.where((pd.notnull(funding_df)), None)
    funding_for_country = funding_df.loc[funding_df['Country'] == country]
    if funding_for_country.empty:
        return 'Error: No funding data was found for this country', 501
    funding_for_country = funding_for_country.iloc[0].to_dict()
    return jsonify(country=country, source=constants.DATA_SOURCES['HNO'], data=funding_for_country)


@app.route('/needs/totals/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_totals_by_country.yml')
def get_needs_totals(country):
    data_keys = ['HNO']
    country = country.strip().capitalize()
    needs_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'hno_needs_total_2017.csv']), encoding='utf-8')
    needs_for_country = needs_df.loc[needs_df['Country'] == country]
    if needs_for_country.empty:
        return 'Error: No needs data was found for this country', 501
    needs_for_country = needs_for_country.iloc[0]
    needs_for_country['Additional Data'] = ast.literal_eval(needs_for_country['Additional Data'])
    needs_for_country = needs_for_country.to_dict()
    needs_iom_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'iom_dtm14_needs_feb2017.csv']), encoding='utf-8')
    needs_iom_for_country = needs_iom_df.loc[needs_iom_df['Country'] == country]
    if not needs_iom_for_country.empty:
        needs_iom_for_country = needs_iom_for_country.iloc[0]
        needs_iom_for_country['Percent Main Unmet Need'] = ast.literal_eval(needs_iom_for_country['Percent Main Unmet Need'])
        needs_iom_for_country['Percent Main Cause Of Displacement'] = ast.literal_eval(needs_iom_for_country['Percent Main Cause Of Displacement'])
        needs_iom_for_country['Regional Summary'] = ast.literal_eval(needs_iom_for_country['Regional Summary'])
        needs_iom_for_country = needs_iom_for_country.to_dict()
        needs_for_country['Additional Data'].update(needs_iom_for_country)
        data_keys.append('DTM')
    # TODO: include 'merged_lake-chad-basin-fts-appeal-data_lake-chad-basin-key-figures-january-2017.csv' data
    #needs_categories_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'merged_lake-chad-basin-fts-appeal-data_lake-chad-basin-key-figures-january-2017.csv']), encoding='utf-8')
    #needs_categories_for_country = needs_categories_df.loc[needs_categories_df['Country'] == country]
    sources = [constants.DATA_SOURCES[data_key] for data_key in data_keys]
    return jsonify(country=country, source=sources, data=needs_for_country)


@app.route('/funding/categories/<string:country>/', methods=['GET'])
@swag_from('api_configs/funding_categories_by_country.yml')
def get_funding_categories(country):
    country = country.strip().capitalize()
    hno_funding_file = 'hno_funding_%s_2017.csv' % country.lower()
    print hno_funding_file
    funding_df = None
    try:
        funding_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, hno_funding_file]), encoding='utf-8')
    except:
        return 'Error: No funding data was found for this country (no file)', 501
    if funding_df.empty:
        return 'Error: No funding data was found for this country (empty file)', 501
    funding_df = funding_df.where((pd.notnull(funding_df)), None)
    funding_dict = funding_df.to_dict(orient='list')
    return jsonify(country=country, source=constants.DATA_SOURCES['HNO'], data=funding_dict)


@app.route('/needs/regions/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_regions_by_country.yml')
def get_needs_regions(country):
    country = country.strip().capitalize()
    idp_country_file = 'idp_%s.csv' % country.lower()
    needs_df = None
    try:
        needs_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, idp_country_file]), encoding='utf-8')
    except:
        return 'Error: No regional needs data was found for this country  (no file)', 501
    if needs_df.empty:
        return 'Error: No regional needs data was found for this country (empty file)', 501
    needs_df = needs_df.where((pd.notnull(needs_df)), None)
    needs_df['PeriodDate'] = pd.to_datetime(needs_df['Period'])
    needs_df.sort_values(by=['ReportedLocation', 'PeriodDate'], inplace=True)
    dates = needs_df['Period'].unique().tolist()
    regions = needs_df['ReportedLocation'].unique().tolist()
    displacement_types = needs_df['DisplType'].unique().tolist()
    # Construct a dict for region name -> displacement type -> list of totals where index corresponds to dates list
    values = {}
    region_groups = needs_df.groupby('ReportedLocation')
    for region, group in region_groups:
        group_df = pd.DataFrame(group).reset_index()
        idp = group_df[group_df.DisplType == 'idp']['TotalTotal'].tolist()
        refugee = group_df[group_df.DisplType == 'refugee']['TotalTotal'].tolist()
        values[region] = {'IDP': idp, 'Refugee': refugee}
    data = {}
    data['dates'] = dates
    data['values'] = values
    return jsonify(country=country, source="TODO: Figure out the original source (from HDX)", data=data)


if __name__ == '__main__':
    app.run(debug=True)
