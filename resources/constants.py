import os.path
# Constants

# TODO: make these relative paths
BASE_DATA_PATH = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data'
RAW_DATA_PATH = os.path.join(BASE_DATA_PATH, 'raw')
DERIVED_DATA_PATH = os.path.join(BASE_DATA_PATH, 'derived')
LATEST_RAW_DATA_PATH = os.path.join(RAW_DATA_PATH, 'latest')
LATEST_RAW_RUN_DATE_FILE = os.path.join(LATEST_RAW_DATA_PATH, 'run_dates.txt')
LATEST_DERIVED_DATA_PATH = os.path.join(DERIVED_DATA_PATH, 'latest')
LATEST_DERIVED_RUN_DATE_FILE = os.path.join(LATEST_DERIVED_DATA_PATH, 'run_dates.txt')
EXAMPLE_RAW_DATA_PATH = os.path.join(RAW_DATA_PATH, 'example')
EXAMPLE_DERIVED_DATA_PATH = os.path.join(DERIVED_DATA_PATH, 'example')

# Standard name for a column of country names
COUNTRY_COL = 'Country'

# Map of country codes to country names, ISO 3166-1 alpha-3 (similar to UNDP and NATO standards)
# TODO: verify which country code standard the int'l dev community actually uses
COUNTRY_CODES = {
  'CHD': 'Chad',
  'CMR': 'Cameroon',
  'NER': 'Niger',
  'NGR': 'Nigeria'
}

# Metadata on original data sources
DATA_SOURCES = {
  'HNO': 'UN OCHA Humanitarian Needs Overview Jan 2017',
  'DTM': 'IOM, NEMA, SEMA, Red Cross: Displacement Tracking Matrix, Round XIV Jan 2017',
  'ORS': 'Online Reporting System run by UN OCHA ROWCA (via HDX)',
  'FTS': 'Financial Tracking Service run by UN OCHA'
}

# HDX website environments, in order of priority to pull data from (i.e. always try 'prod' first)
HDX_SITES = ['prod', 'feature', 'test']

# HDX data
HDX_DATASETS = [
  'lcb-displaced', 
  'lake-chad-basin-fts-appeal-data',
  'lake-chad-basin-key-figures-january-2017'  # This Dataset has multiple Resources
  #'conflict-events',
  #'lake-chad-basin-baseline-population',
  #'lac-chad-basin-area'  # zipped shapefiles
]

# Based off of HDX expected update frequency keywords (required for each Dataset)
UPDATE_FREQUENCY = [
  'Every day',
  'Every week',
  'Every two weeks',
  'Every month',
  'Every three months',
  'Every six months',
  'Every year',
  'Never',
  'Unknown / Irregular'
]

# UNHCR sub-directory (e.g. under data/raw/latest)
UNHCR_DIR = 'unhcr'

# FTS sub-directory (e.g. under data/raw/latest)
FTS_DIR = 'fts'

# FTS data download date file
FTS_DOWNLOAD_DATE_FILE = 'download_date.txt'

# FTS data file prefix
FTS_FILE_PREFIX = 'fts-appeals'

# FTS data schemas
FTS_SCHEMAS = {
  'donors': ['Donor organization', 'Funding US$', 'Pledges US$'],
  'clusters': ['Cluster/Sector', 'Requirements US$', 'Funding US$', 'Coverage %'],
  'recipients': ['Recipient organization', 'Requirements US$', 'Funding US$', 'Pledges US$', 'Coverage %']
}

# DTM column names referring to states within a country
DTM_STATE_COLS = {
  'location': 'STATE',
  'site': 'STATE',
  'baseline': 'state_name'
}

# DTM file mapping (temporary for now)
# TODO: make file names generic including DTM assessment type to remove the need for this config
DTM_FILE_NAMES = {
  'location': '14_DTM_NIgeria_Round_XIV_Dataset_of_Location_Assessment.csv',
  'site': '06_DTM_Nigeria_Round_XIV_Dataset_of_Site_Assessment.csv',
  'baseline': 'wards_05_DTM_Nigeria_Round_XIV_Dataset_of_Baseline_Assessment.csv'
}

