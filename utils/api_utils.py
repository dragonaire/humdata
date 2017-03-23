import pandas as pd
from resources import constants


def safely_load_data(data_file, data_description, filter_value=None, filter_column=constants.COUNTRY_COL):
    """
    Attempt to load the data_file as a pandas dataframe (df).
    Return a tuple of whether it was successful, and either the df if it's successful, or an error message if it's not.
    """
    success = False
    result = None
    try:
        result = pd.read_csv('/'.join([constants.EXAMPLE_DERIVED_DATA_PATH, data_file]), encoding='utf-8')
        success = True
        if result.empty:
            result = 'Error: No {} data was found (empty file)'.format(data_description)
            success = False
        elif filter_value:
            result = result.loc[result[filter_column] == filter_value]
            if result.empty:
                result = 'Error: No {} data was found for the filter [{}: {}] (empty file)'.format(data_description, filter_column, filter_value)
                success = False
    except Exception as e:
        result = 'Error: No {} data was found ({})'.format(data_description, e)
        success = False

    if success:
        result = result.where((pd.notnull(result)), None)

    return success, result

