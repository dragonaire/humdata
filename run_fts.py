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


def updateLatestDataDir(download_path, current_date_str):
    """
    Copies all files from the given download_path into the latest data directory configured in
    `resources/constants.py`. Appends to the run_dates.txt file with the current run date.
    """
    if not download_path or not current_date_str:
        print 'Could not copy latest data for this run to the latest data directory!'
        return
    dir_util.copy_tree(download_path, constants.LATEST_DERIVED_DATA_PATH)
    with open(constants.LATEST_DERIVED_RUN_DATE_FILE, 'a') as run_file:
        run_file.write('{}-fts\n'.format(current_date_str))
    return


def createCurrentDateDir(parent_dir):
    """
    Create a new directory with the current date (ISO format) under the given parent_dir.
    Return whether it was successful, the full path for the new directory, and the current date string.
    If the date directory already exists or is not successful, default to returning the parent_dir as the full path.
    """
    # Create a new directory of the current date under the given parent_dir if it doesn't already exist
    current_date_str = date.today().isoformat()
    dir_path = os.path.join(parent_dir, current_date_str)
    success = data_utils.safely_mkdir(dir_path)
    if not success:
        # TODO: handle this better
        # Safely default to returning the parent_dir if we cannot create the dir_path
        print 'Could not create a new directory for the current date [{}], defaulting to existing parent dir: {}'.format(current_date_str, parent_dir)
        dir_path = parent_dir
    else:
        print 'Created new derived data dir: {}'.format(dir_path)
    return success, dir_path, current_date_str


def saveDerivedData(data, dir_path):
    """
    Save the derived data into a new dated directory under the given parent_dir (defaults to DERIVED_DATA_PATH configured in `resources/constants.py`).
    Return whether any data saving was successful.
    """
    # Save data to dated directory under the given parent_dir
    success = False
    for dimension, df in data.iteritems():
        df_path = os.path.join(dir_path, 'fts-{}.csv'.format(dimension))
        print 'Saving derived data for dimension [{}] to: {}'.format(dimension, df_path)
        df.to_csv(df_path, index=False, encoding='utf-8')
        success = True
    return success


def run():
    print 'Load and process downloaded data from FTS'
    # Create current date directory
    print 'Create current date directory as the download path...'
    _, download_path, current_date_str = createCurrentDateDir(constants.DERIVED_DATA_PATH)
    print 'Load data by dimension...'
    data_by_dimension = {}
    for dimension, schema in constants.FTS_SCHEMAS.iteritems():
        data_for_dimension = loadDataByDimension(dimension)
        print 'Combine data for dimension [{}] across all countries...'.format(dimension)
        data_by_dimension[dimension] = combineData(data_for_dimension, constants.COUNTRY_COL)
        print data_by_dimension[dimension]

    success = saveDerivedData(data_by_dimension, download_path)
    if success:
        print 'Copy data from {} to {}...'.format(download_path, constants.LATEST_DERIVED_DATA_PATH)
        updateLatestDataDir(download_path, current_date_str)
    
    #dir_util.copy_tree(download_path, constants.EXAMPLE_DERIVED_DATA_PATH)

    print 'Done!'


if __name__ == "__main__":
    run()
