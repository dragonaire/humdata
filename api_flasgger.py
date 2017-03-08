from flask import Flask, jsonify, request
from flasgger import Swagger
import pandas as pd


app = Flask(__name__)
api = Swagger(app)

@app.route('/humdata/funding/<string:country>/', methods=['GET'])
def getFunding(country):
    """
    Humanitarian Data Service
    Call this endpoint to get the funding data for a given country
    ---
    tags:
      - Humanitarian Data Service
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
            data:
              type: json
              description: The funding data
              default: {'Country': 'Chad', 'Requirement 2016': 98205277, 'Funded 2016': 54276412, 'Percent Funded 2016': 0.55000000000000004, 'Requirement 2017': 121261684, 'Tagged For Refugee Response': 16723548.0}
    """
    country = country.strip().capitalize()
    data_dir = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data/derived'
    funding_df = pd.read_csv('/'.join([data_dir, 'hno_funding_2016_2017.csv']), encoding='utf-8')
    funding_df = funding_df.where((pd.notnull(funding_df)), None)
    funding_for_country = funding_df.loc[funding_df['Country'] == country]
    if funding_for_country.empty:
        return 'Error: No funding data was found for this country', 501
    funding_for_country = funding_for_country.iloc[0].to_dict()
    return jsonify(country=country, data=funding_for_country)


if __name__ == '__main__':
    app.run(debug=True)
