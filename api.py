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


@app.route('/totals/funding/<string:country>/', methods=['GET'])
@swag_from('total_funding_by_country.yml')
def get_funding(country):
    country = country.strip().capitalize()
    funding_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'hno_funding_2016_2017.csv']), encoding='utf-8')
    funding_df = funding_df.where((pd.notnull(funding_df)), None)
    funding_for_country = funding_df.loc[funding_df['Country'] == country]
    if funding_for_country.empty:
        return 'Error: No funding data was found for this country', 501
    funding_for_country = funding_for_country.iloc[0].to_dict()
    return jsonify(country=country, source=constants.DATA_SOURCES['HNO'], data=funding_for_country)


@app.route('/totals/needs/<string:country>/', methods=['GET'])
def get_needs(country):
    """
    Get needs data for a country
    Call this endpoint to get the people-in-need data totals for a given country
    ---
    tags:
      - Lake Chad Basin
    parameters:
      - name: country
        in: path
        type: string
        required: true
        description: The country name (slugified, i.e. no special characters)
    responses:
      501:
        description: No needs data was found for this country
      200:
        description: The latest needs data (estimated to the thousands of people) for the given country
        schema:
          id: needs
          properties:
            country:
              type: string
              description: The country name
              default: Chad
            source:
              type: array
              description: The data sources
              items:
                type: string
              default: ["UN OCHA Humanitarian Needs Overview 2017", "IOM", "ACLED", "UNHCR"]
            data:
              type: json
              description: The needs data
              default: {'Country': 'Chad', 'People In Need': 345000, 'People Targeted For Assistance': 233000}
    """
    country = country.strip().capitalize()
    needs_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'hno_needs_total_2017.csv']), encoding='utf-8')
    needs_for_country = needs_df.loc[needs_df['Country'] == country]
    if needs_for_country.empty:
        return 'Error: No needs data was found for this country', 501
    needs_for_country = needs_for_country.iloc[0]
    needs_for_country['Additional Data'] = ast.literal_eval(needs_for_country['Additional Data'])
    # TODO: include 'merged_lake-chad-basin-fts-appeal-data_lake-chad-basin-key-figures-january-2017.csv' data
    # needs_categories_df = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, 'merged_lake-chad-basin-fts-appeal-data_lake-chad-basin-key-figures-january-2017.csv']), encoding='utf-8')
    # needs_categories_for_country = needs_categories_df.loc[needs_categories_df['Country'] == country]
    return jsonify(country=country, source=constants.DATA_SOURCES['HNO'], data=needs_for_country.to_dict())


# @app.route('/totals/needs/<string:country>/', methods=['GET'])
# def getNeeds(country):


if __name__ == '__main__':
    app.run(debug=True)
