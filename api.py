import sys
import ast
import pandas as pd
from flask import Flask, jsonify, request
from flasgger import Swagger
from flasgger.utils import swag_from

from resources import constants
from utils import api_utils


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
    # Background colors: https://uigradients.com/#GrapefruitSunset
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
    success, result = api_utils.safely_load_data('hno_funding_2016_2017.csv', 'funding', country)
    if not success:
        return result, 501
    result = result.iloc[0].to_dict()
    return jsonify(country=country, source=constants.DATA_SOURCES['HNO'], data=result, update=constants.UPDATE_FREQUENCY[3])


@app.route('/funding/categories/<string:country>/', methods=['GET'])
@swag_from('api_configs/funding_categories_by_country.yml')
def get_funding_categories(country):
    country = country.strip().capitalize()
    hno_funding_file = 'hno_funding_%s_2017.csv' % country.lower()
    success, result = api_utils.safely_load_data(hno_funding_file, 'category funding')
    if not success:
        return result, 501
    result = result.to_dict(orient='list')
    return jsonify(country=country, source=constants.DATA_SOURCES['HNO'], data=result, update=constants.UPDATE_FREQUENCY[3])


def get_funding_by_fts_dimension(country, fts_dimension):
    """
    Helper function for FTS funding endpoints.
    Returns whether data retrieval was successful (or http errorcode if not), and the resulting json data (or error message if not).
    """
    country = country.strip().capitalize()
    fts_donors_file = 'fts-{}.csv'.format(fts_dimension)
    success, result = api_utils.safely_load_data(fts_donors_file, '{} funding'.format(fts_dimension), country)
    if not success:
        return 501, result
    result.drop(constants.COUNTRY_COL, axis=1, inplace=True)
    return success, result.to_dict(orient='list')


@app.route('/funding/donors/<string:country>/', methods=['GET'])
@swag_from('api_configs/funding_donors_by_country.yml')
def get_funding_donors(country):
    country = country.strip().capitalize()
    success, result = get_funding_by_fts_dimension(country, 'donors')
    if not success or success == 501:
        return result, 501
    return jsonify(country=country, source=constants.DATA_SOURCES['FTS'], data=result, update=constants.UPDATE_FREQUENCY[2])


@app.route('/funding/clusters/<string:country>/', methods=['GET'])
@swag_from('api_configs/funding_clusters_by_country.yml')
def get_funding_clusters(country):
    country = country.strip().capitalize()
    success, result = get_funding_by_fts_dimension(country, 'clusters')
    if not success or success == 501:
        return result, 501
    return jsonify(country=country, source=constants.DATA_SOURCES['FTS'], data=result, update=constants.UPDATE_FREQUENCY[2])


@app.route('/funding/recipients/<string:country>/', methods=['GET'])
@swag_from('api_configs/funding_recipients_by_country.yml')
def get_funding_recipients(country):
    country = country.strip().capitalize()
    success, result = get_funding_by_fts_dimension(country, 'recipients')
    if not success or success == 501:
        return result, 501
    return jsonify(country=country, source=constants.DATA_SOURCES['FTS'], data=result, update=constants.UPDATE_FREQUENCY[2])


@app.route('/needs/totals/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_totals_by_country.yml')
def get_needs_totals(country):
    data_keys = ['HNO']
    country = country.strip().capitalize()

    success, result = api_utils.safely_load_data('hno_needs_total_2017.csv', 'needs', country)
    if not success:
        return result, 501
    result = result.iloc[0]
    result = result.to_dict()
    result['Additional Data'] = ast.literal_eval(result['Additional Data'])

    success, iom = api_utils.safely_load_data('iom_dtm14_needs_feb2017.csv', 'IOM needs', country)
    if success:
        iom = iom.iloc[0].to_dict()
        iom['Percent Main Unmet Need'] = ast.literal_eval(iom['Percent Main Unmet Need'])
        iom['Percent Main Cause Of Displacement'] = ast.literal_eval(iom['Percent Main Cause Of Displacement'])
        iom['Regional Summary'] = ast.literal_eval(iom['Regional Summary'])
        result['Additional Data'].update(iom)
        data_keys.append('DTM')

    sources = [constants.DATA_SOURCES[data_key] for data_key in data_keys]
    return jsonify(country=country, source=sources, data=result, update=constants.UPDATE_FREQUENCY[3])


@app.route('/needs/regions/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_regions_by_country.yml')
def get_needs_regions(country):
    country = country.strip().capitalize()
    success, result = api_utils.safely_load_data('lcb_displaced_2017.csv', 'regional needs', country)
    if not success:
        return result, 501
    result['PeriodDate'] = pd.to_datetime(result['Period'])
    result.sort_values(by=['ReportedLocation', 'PeriodDate'], inplace=True)
    dates = result['Period'].unique().tolist()
    regions = result['ReportedLocation'].unique().tolist()
    displacement_types = result['DisplType'].unique().tolist()
    # Construct a dict for region name -> displacement type -> list of totals where index corresponds to dates list
    values = {}
    region_groups = result.groupby('ReportedLocation')
    for region, group in region_groups:
        group_df = pd.DataFrame(group).reset_index()
        idp = group_df[group_df.DisplType == 'idp']['TotalTotal'].tolist()
        refugee = group_df[group_df.DisplType == 'refugee']['TotalTotal'].tolist()
        values[region] = {'IDP': idp, 'Refugee': refugee}
    data = {}
    data['dates'] = dates
    data['values'] = values
    return jsonify(country=country, source=constants.DATA_SOURCES['ORS'], data=data, update=constants.UPDATE_FREQUENCY[-1])


def get_needs_assessment_by_type(country='Nigeria', state='Borno', dtm_assessment_type='baseline'):
    """
    Helper function for DTM needs assessment endpoints.
    Returns whether data retrieval was successful (or http errorcode if not), and the resulting json data (or error message if not).
    """
    country = country.strip().capitalize()
    if country != 'Nigeria':
        return 501, 'This country [{}] is currently not supported for site assessment data'.format(country)
    dtm_file = constants.DTM_FILE_NAMES[dtm_assessment_type]
    state_col = constants.DTM_STATE_COLS[dtm_assessment_type]
    success, result = api_utils.safely_load_data(dtm_file, 'site assessment needs', state.upper(), state_col)
    if not success:
        return 501, result
    result.drop(state_col, axis=1, inplace=True)
    result = result.to_dict(orient='list')
    return success, result


@app.route('/needs/assessment/site/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_assessment_site_by_state.yml')
def get_needs_assessment_site(country):
    # Note: this endpoint is only available for Nigeria for now, and assumes states in Nigeria
    country = country.strip().capitalize()
    dtm_assessment_type = 'site'
    state = str(request.args.get('state', 'Borno')).strip().capitalize()
    success, result = get_needs_assessment_by_type(country, state, dtm_assessment_type)
    if not success or success == 501:
        return result, 501
    return jsonify(country=country, state=state, source=constants.DATA_SOURCES['DTM'], data=result, update=constants.UPDATE_FREQUENCY[3])


@app.route('/needs/assessment/location/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_assessment_location_by_state.yml')
def get_needs_assessment_location(country):
    # Note: this endpoint is only available for Nigeria for now, and assumes states in Nigeria
    country = country.strip().capitalize()
    dtm_assessment_type = 'location'
    state = str(request.args.get('state', 'Borno')).strip().capitalize()
    success, result = get_needs_assessment_by_type(country, state, dtm_assessment_type)
    if not success or success == 501:
        return result, 501
    return jsonify(country=country, state=state, source=constants.DATA_SOURCES['DTM'], data=result, update=constants.UPDATE_FREQUENCY[3])


@app.route('/needs/assessment/baseline/<string:country>/', methods=['GET'])
@swag_from('api_configs/needs_assessment_baseline_by_state.yml')
def get_needs_assessment_baseline(country):
    # Note: this endpoint is only available for Nigeria for now, and assumes states in Nigeria
    country = country.strip().capitalize()
    dtm_assessment_type = 'baseline'
    state = str(request.args.get('state', 'Borno')).strip().capitalize()
    success, result = get_needs_assessment_by_type(country, state, dtm_assessment_type)
    if not success or success == 501:
        return result, 501
    return jsonify(country=country, state=state, source=constants.DATA_SOURCES['DTM'], data=result, update=constants.UPDATE_FREQUENCY[3])


@app.route('/test/<string:country>/', methods=['GET'])
@swag_from('api_configs/test.yml')
def test(country):
    country = country.strip().capitalize()
    success, result = api_utils.safely_load_data('test.csv', 'test')
    if not success:
        return result, 501
    return jsonify(country=country, source='test', data=result.to_dict(), update=constants.UPDATE_FREQUENCY[-1])


def main():
    env_type = 'local'
    if len(sys.argv) == 2:
        env_type = sys.argv[1]
    if env_type == 'remote':
        app.run(debug=True, port=80, host='0.0.0.0')
    else:
        app.run(debug=True)


if __name__ == '__main__':
    main()

