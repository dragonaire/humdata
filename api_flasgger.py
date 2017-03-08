from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd
import ast


app = Flask(__name__)
api = Swagger(app)

# TODO: put this in resources/constants.py
data_dir = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data/derived'
source = 'UN OCHA Humanitrian Needs Overview 2017'

@app.route('/totals/funding/<string:country>/', methods=['GET'])
def getFunding(country):
    """
    Humanitarian Data Service
    Call this endpoint to get the latest funding data (in USD) totals for a given country
    ---
    tags:
      - Humanitarian Data Service
      - funding
      - totals
    parameters:
      - name: country
        in: path
        type: string
        required: true
        description: The country name (slugified, i.e. no special characters)
    responses:
      501:
        description: No funding data was found for this country
      200:
        description: The latest funding data (in USD) for the given country
        schema:
          id: funding
          properties:
            country:
              type: string
              description: The country name
              default: Chad
            source:
              type: string
              description: The data source name
              default: UN OCHA Humanitarian Needs Overview 2017
            data:
              type: json
              description: The funding data
              default: {'Country': 'Chad', 'Requirement 2016': 98205277, 'Funded 2016': 54276412, 'Percent Funded 2016': 0.55000000000000004, 'Requirement 2017': 121261684, 'Tagged For Refugee Response': 16723548.0}
    """
    country = country.strip().capitalize()
    funding_df = pd.read_csv('/'.join([data_dir, 'hno_funding_2016_2017.csv']), encoding='utf-8')
    funding_df = funding_df.where((pd.notnull(funding_df)), None)
    funding_for_country = funding_df.loc[funding_df['Country'] == country]
    if funding_for_country.empty:
        return 'Error: No funding data was found for this country', 501
    funding_for_country = funding_for_country.iloc[0].to_dict()
    return jsonify(country=country, source=source, data=funding_for_country)


@app.route('/totals/needs/<string:country>/', methods=['GET'])
def getNeeds(country):
    """
    Humanitarian Data Service
    Call this endpoint to get the people-in-need data totals for a given country
    ---
    tags:
      - Humanitarian Data Service
      - needs
      - totals
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
              type: string
              description: The data source name
              default: UN OCHA Humanitarian Needs Overview 2017
            data:
              type: json
              description: The needs data
              default: {'Country': 'Chad', 'People In Need': 345000, 'People Targeted For Assistance': 233000}
    """
    country = country.strip().capitalize()
    needs_df = pd.read_csv('/'.join([data_dir, 'hno_needs_total_2017.csv']), encoding='utf-8')
    needs_for_country = needs_df.loc[needs_df['Country'] == country]
    if needs_for_country.empty:
        return 'Error: No needs data was found for this country', 501
    needs_for_country = needs_for_country.iloc[0]
    needs_for_country['Additional Data'] = ast.literal_eval(needs_for_country['Additional Data'])
    return jsonify(country=country, source=source, data=needs_for_country.to_dict())


if __name__ == '__main__':
    app.run(debug=True)
