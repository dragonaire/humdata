import os.path
import pandas as pd
from datetime import date
from distutils import dir_util

from hdx.configuration import Configuration
from hdx.data.dataset import Dataset

from resources import constants
from utils import data_utils


def getDataset(dataset_name):
    """
    An HDX Dataset (sub-URL) is a collection of one or more Resources (raw data files).

    Return the Dataset and its list of Resources.

    Example:
      URL: https://feature-data.humdata.org/dataset/lake-chad-basin-fts-appeal-data
      hdx_site = 'feature'
      dataset_name = 'lake-chad-basin-fts-appeal-data'
      Configuration.create(hdx_site=hdx_site, hdx_read_only=True)  # assumes this is already done
      dataset = Dataset.read_from_hdx(dataset_name)  # downloads the given dataset_name
    """

    print('Get %s Dataset from HDX...' % dataset_name)
    dataset = None
    for site_env in constants.HDX_SITES:
        try:
            print('Try configuration with hdx_site = %s...' % site_env)
            Configuration.create(hdx_site=site_env, hdx_read_only=True)
            dataset = Dataset.read_from_hdx(dataset_name)
        except Exception as e:
            print('Exception when trying to read dataset from env [%s]: %s!' % (site_env, e))
        else:
            if not dataset:
                print('Configuration works but dataset name [%s] does not exist!' % dataset_name)
            else:
                print('Successfully found dataset from env [%s]: [%s]' % (site_env, dataset_name))
                break

    if not dataset:
        print('Dataset [%s] does not exist despite trying all hdx_site envs!' % dataset_name)
        raise  

    print('Extract metadata from dataset:')
    #print(dataset.get_dataset_date())  # This doesn't always exist, optional? what is guaranteed?
    print(dataset.get_expected_update_frequency())  # This should b guaranteed, see c`constants.py`
    print(dataset.get_location())
    print(dataset.get_tags())

    print('Get number of resources from dataset...')
    resources = dataset.resources
    print(len(resources))

    print('Done downloading this dataset')
    return dataset, resources


def downloadResources(resources, download_path=constants.RAW_DATA_PATH):
    """
    Given a list of HDX Resources, download its Resource files and load them as pandas dataframes.
    Return a dictionary of Resource filenames and their corresponding loaded pandas dataframes.
    Note: this assumes all resources are csv files, and calls the function loadResourceFromPath().
    """
    print('Load %d resources' % len(resources))

    resource_dfs = {}
    for resource in resources:
        resource_url, resource_path = resource.download(download_path)
        print('Resource URL %s downloaded to %s' % (resource_url, resource_path))
        resource_filename = os.path.basename(resource_path)
        resource_dfs[resource_filename] = loadResourceFromPath(resource_path)

    print('Done downloading this list of resources')
    return resource_dfs


def loadResourceFromPath(resource_path):
    """
    Given the full path, load a downloaded Resource csv file as a pandas dataframe.
    Drop the first row, which is the HXL metadata tag (often a desription of the column names).
    """

    print('Load Resource path...')
    res = pd.read_csv(resource_path, encoding='utf-8')

    # Drop the first row which is always HXL metadata from HDX
    res.drop(0, inplace=True)

    print(res.columns)
    print(res.head())

    return res


# TODO: support the case when you want to merge on multiple columns (e.g. country and date)
def joinResources(res1, res1_cols, res2, res2_cols, merge_key=None, merge_fn=None):
    """
    Given two Resources (loaded as pandas dataframes) and their columns to join on,
    merge them on the specified column according to the merge_key using the specified merging function.
    If no merging function is specified, default to a naive left join on top of the first Resource.
    """

    # Extract the merge columns
    res1_mcol = list(res1_cols.values())[0]
    res2_mcol = list(res2_cols.values())[0]
    if merge_key:
        res1_mcol = res1_cols[merge_key]
        res2_mcol = res2_cols[merge_key]

    # Preprocess resources (cleaning, etc)
    # TODO: first check if dtype is string before running .strip()
    #res1_col_val = res1.sort_values(res1_mcol, ascending=True)[res1_mcol].iloc[0]
    #res2_col_val = res2.sort_values(res2_mcol, ascending=True)[res2_mcol].iloc[0]
    #if res1_col_val.istype(str) and res2_col_val.istype(str):  # TODO: fix this to compile
    #    res1[res1_mcol] = res1[res1_mcol].apply(lambda r: r.strip())
    #    res2[res2_mcol] = res2[res2_mcol].apply(lambda r: r.strip())

    # TODO: throw Exception if a sanity check fails...is this too harsh?
    # how to safely handle ambiguity problems while still bubbling the problem
    # Sanity check Resources:
    #   - same number of unique values for columns to merge?
    res1_col_uniq = res1[res1_mcol].nunique()
    res2_col_uniq = res2[res2_mcol].nunique()
    if res1_col_uniq != res2_col_uniq:
        print('Ambiguous: Columns to merge do not have the same number of unique values!')
    #  - if values don't match in sorted dataframe, is there a custom merge_fn specified?
    res1_col_val = res1.sort_values(res1_mcol, ascending=True)[res1_mcol].iloc[0]
    res2_col_val = res2.sort_values(res2_mcol, ascending=True)[res2_mcol].iloc[0]
    merged_res = None
    if res1_col_val != res2_col_val and not merge_fn:
        print('Ambiguous: Missing custom merge function despite column values not matching!')
    elif res1_col_val != res2_col_val:
        # Column values do not match, use the custom merge_fn to merge
        merged_res = merge_fn(res1, res1_cols, res2, res2_cols, merge_key)
    else:
        # Column values match, proceed with direct merge
        merged_res = res1.merge(res2, how='outer', left_on=res1_mcol, right_on=res2_mcol)
        
    return merged_res


def mergeByCountryLatestDate(res1, res1_cols, res2, res2_cols, merge_key='country'):
    """
    Filter for rows with latest dates by country, and replace country code with country_code dictionary (i.e. full country name)
    before doing a full outer join to merge the two.
    Note: res1_cols and res2_cols should both be dictionaries mapping the 'country' and 'date' columns for each res.
    """

    # Sanity check that resn_cols are as expected
    if ('date' not in res1_cols.keys()) or ('date' not in res2_cols.keys()):
        print('Invalid: cannot filter for latest date without a date column specified for a resource!')
    elif (merge_key not in res1_cols.keys()) or (merge_key not in res2_cols.keys()):
        print('Invalid: cannot merge by country without a country column specified for a resource!')
    else:
        # Arguments are as expected
        pass

    # Figure out which df has country codes, replace with full country names
    res1_country_sample = res1[res1_cols['country']].iloc[0]
    res2_country_sample = res2[res2_cols['country']].iloc[0]
    if res1_country_sample in constants.COUNTRY_CODES.keys():
        res1.replace({res1_cols['country']: constants.COUNTRY_CODES}, inplace=True)
    elif res2_country_sample in constants.COUNTRY_CODES.keys():
        res2.replace({res2_cols['country']: constants.COUNTRY_CODES}, inplace=True)
    else:
        # Assume columns have the same country values, no need to replace, just merge directly
        pass

    # Get latest dates and filter df's for just the latest info
    # Example: 
    # res_latest = {'CHD': '2017-01-11', 'CMR': '2017-01-11'}
    res1_latest = res1.groupby(res1_cols['country']).agg({res1_cols['date']: 'max'}).to_dict()[res1_cols['date']]
    res2_latest = res2.groupby(res2_cols['country']).agg({res2_cols['date']: 'max'}).to_dict()[res2_cols['date']]
    # Filter df for just the latest info by country (should end up with one row per country, the row with the latest date)
    res1 = res1[res1[list(res1_cols.values())].apply(lambda r: r[res1_cols['date']] == res1_latest[r[res1_cols['country']]], axis=1)]
    res2 = res2[res2[list(res2_cols.values())].apply(lambda r: r[res2_cols['date']] == res2_latest[r[res2_cols['country']]], axis=1)]

    merged_res = res1.merge(res2, how='outer', left_on=res1_cols['country'], right_on=res2_cols['country'])
    return merged_res


def createCurrentDateDir(parent_dir):
    """
    Create a new directory with the current date (ISO format) under the given parent_dir.
    Return whether it was successful, the full path for the new directory, and the current date string.
    If the date directory already exists or is not successful, default to returning the parent_dir as the full path.
    """
    current_date_str = date.today().isoformat()
    dir_path = os.path.join(parent_dir, current_date_str)
    success = data_utils.safely_mkdir(dir_path)
    if not success:
        # Safely default to returning the parent_dir if we cannot create the dir_path
        print('Could not create a new directory for the current date [%s], defaulting to existing parent dir' % current_date_str)
        dir_path = parent_dir
    else:
        print("Created new raw data dir: %s" % dir_path)
    return success, dir_path, current_date_str


def updateLatestDataDir(download_path, current_date_str):
    """
    Copies all files from the given download_path into the latest data directory configured in
    `resources/constants.py`. Appends to the run_dates.txt file with the current run date.
    """
    if not download_path or not current_date_str:
        print('Could not copy latest data for this run to the latest data directory!')
        return
    dir_util.copy_tree(download_path, constants.LATEST_RAW_DATA_PATH)
    with open(constants.LATEST_RAW_RUN_DATE_FILE, 'a') as run_file:
        run_file.writelines(current_date_str)
    return


def run():
    print('Download and merge data from HDX')
    datasets = {}
    resources = {}
    # Create current date directory
    print('Create current date directory as the download path...')
    _, download_path, current_date_str = createCurrentDateDir(constants.RAW_DATA_PATH)
    # Download resources
    print('Download Resources...')
    num_resources = 0
    is_new_data = False
    for dataset_name in constants.HDX_DATASETS:
        resource_list = None
        try:
            dataset, resource_list = getDataset(dataset_name)
            datasets[dataset_name] = dataset
            resource_dfs = downloadResources(resource_list, download_path)
            resources[dataset_name] = resource_dfs
            num_resources = num_resources + len(resource_dfs)
            if not is_new_data and len(resource_dfs):
                is_new_data = True
        except Exception as e:
            print('Exception: could not reach the HDX API to download data!')
            print(e)

    if is_new_data:
        updateLatestDataDir(download_path, current_date_str)

    print('== Num datasets configured: %d ==' % len(constants.HDX_DATASETS))
    print('== Num datasets downloaded: %d ==' % len(datasets))
    print('== Num resources loaded: %d ==' % num_resources)
    print('ALL RESOURCES:')
    #print(resources)
    for dataset_name, resource_dfs in resources.items():
        print('Dataset: %s' % dataset_name)
        print('Resources for dataset: %s' % list(resource_dfs.keys()))

    # Join resources
    #print('Join Resources...')
    #res1_cols = {'country': 'country', 'date': 'end_date'}
    #res2_cols = {'country': 'Country', 'date': 'Date'}
    #res1_df = resources['lake-chad-basin-fts-appeal-data']['Lake_Chad_Basin_Appeal_Status_2016-08-31.csv']
    #res2_df = resources['lake-chad-basin-key-figures-january-2017']['LCB_SnapShot_DataSets_24Jan17.xlsx---key_figures.csv']
    #merged_resource = joinResources(res1_df, res1_cols, res2_df, res2_cols, 'country', mergeByCountryLatestDate)
    #print('Merged resource from %s and %s:' % (dataset_names[1], dataset_names[2]))
    #print(merged_resource.head())
    #merged_resource.to_csv('/'.join([constants.RAW_DATA_PATH, 'merged_%s_%s.csv' % (dataset_names[1], dataset_names[2])]), index=False)

    print('Done!')


if __name__ == "__main__":
    run()
