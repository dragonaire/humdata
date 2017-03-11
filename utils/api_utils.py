import pandas as pd
from resources import constants


def safely_load_data(data_file, data_description, country_filter=None):
    """
    Attempt to load the data_file as a pandas dataframe (df).
    Return a tuple of whether it was successful, and either the df if it's successful, or an error message if it's not.
    """
    success = False
    result = None
    try:
        result = pd.read_csv('/'.join([constants.DERIVED_DATA_PATH, data_file]), encoding='utf-8')
        success = True
        if result.empty:
            result = 'Error: No %s data was found for this country (empty file)' % data_description
            success = False
        elif country_filter:
            # TODO: make sure that derived data sets all have uniform "Country" header for country
            result = result.loc[result['Country'] == country_filter]
            if result.empty:
                result = 'Error: No %s data was found for this country (empty file)' % data_description
                success = False
    except Exception as e:
        result = 'Error: No %s data was found for this country (%s)' % (data_description, e)
        success = False

    if success:
        result = result.where((pd.notnull(result)), None)

    return success, result

