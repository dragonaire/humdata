import os.path
import pandas as pd
from datetime import date
from distutils import dir_util

from resources import constants
from utils import data_utils


def loadDataByDimension(dimension):
    """
    Given a dimension of funding data (e.g. clusters/donors/recipients), load the data for each country.
    Return a dict of country code to pandas dataframe for the funding data along the given dimension.
    """
    if dimension not in constants.FTS_SCHEMAS.keys():
        raise Exception('Not a valid funding dimension for downloaded data from FTS: {}!'.format(dimension))
    schema = constants.FTS_SCHEMAS[dimension]
    data_dir = os.path.join(constants.LATEST_RAW_DATA_PATH, constants.FTS_DIR)
    date_str = date.today().isoformat()
    with open(os.path.join(data_dir, constants.FTS_DOWNLOAD_DATE_FILE), 'r') as f:
        date_str = f.read().strip()
    data = {}
    for code, country in constants.COUNTRY_CODES.iteritems():
        print country
        file_name = '-'.join([constants.FTS_FILE_PREFIX, code, dimension, date_str])
        file_path = os.path.join(data_dir, '{}.csv'.format(file_name))
        df = pd.read_csv(file_path, encoding='utf-8')
        data[country] = df
    return data


def loadDataByCountryCode(country_code):
    """
    Given a country, load the data for each funding dimension.
    Return a dict of funding dimension to pandas dataframe for the funding data for the given country.
    """
    if country_code not in constants.COUNTRY_CODES.keys():
        if country_code not in constants.COUNTRY_CODES.values():
            raise Exception('Not a valid country code for downloaded data from FTS: {}!'.format(country))
        else:
            # Convert country name to country code
            country_code = constants.COUNTRY_CODES.values().index(country_code)

    data_dir = os.path.join(constants.LATEST_RAW_DATA_PATH, constants.FTS_DIR)
    date_str = date.today().isoformat()
    with open(os.path.join(data_dir, constants.FTS_DOWNLOAD_DATE_FILE), 'r') as f:
        date_str = f.read().strip()
    data = {}
    for dimension, schema in constants.FTS_SCHEMAS.iteritems():
        file_name = '-'.join([constants.FTS_FILE_PREFIX, country_code, dimension, date_str])
        file_path = os.path.join(data_dir, '{}.csv'.format(file_name))
        df = pd.read_csv(file_path, encoding='utf-8')
        data[dimension] = df
    return data


def combineData(data, column):
    """
    Combine given data across a particular column, where data is a dictionary from keys to dataframes,
    and the given column corresponds to a column name for the keys of the data dict, e.g. 'Country' or 'Dimension'.
    Returns a single dataframe that combines all the dataframes in the given data.
    """
    combined_df = pd.DataFrame()
    for key, df in data.iteritems():
        df[column] = key
        combined_df = combined_df.append(df)
    return combined_df


def run():
    print 'Load and process downloaded data from FTS'
    print 'Load data by dimension...'
    dimension_column_name = 'Funding Dimension'
    data_by_dimension = {}
    for dimension, schema in constants.FTS_SCHEMAS.iteritems():
        data_for_dimension = loadDataByDimension(dimension)
        print 'Combine data for dimension [{}] across all countries...'.format(dimension)
        data_by_dimension[dimension] = combineData(data_for_dimension, dimension_column_name)
        print data_by_dimension[dimension]

    # TODO:for each dimension, save the df = data_by_dimension[dimension] in data/derived/latest and <dated_dir>

    print 'Done!'


if __name__ == "__main__":
    run()
