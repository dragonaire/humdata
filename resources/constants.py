# Constants

# TODO: make these relative paths
BASE_DATA_PATH = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data'
RAW_DATA_PATH = '/'.join([BASE_DATA_PATH, 'raw'])
DERIVED_DATA_PATH = '/'.join([BASE_DATA_PATH, 'derived'])
LATEST_RAW_DATA_PATH = '/'.join([RAW_DATA_PATH, 'latest'])
LATEST_RAW_RUN_DATE_FILE = '/'.join([LATEST_RAW_DATA_PATH, 'run_dates.txt'])
LATEST_DERIVED_DATA_PATH = '/'.join([DERIVED_DATA_PATH, 'latest'])
LATEST_DERIVED_RUN_DATE_FILE = '/'.join([LATEST_DERIVED_DATA_PATH, 'run_dates.txt'])
EXAMPLE_RAW_DATA_PATH = '/'.join([RAW_DATA_PATH, 'example'])
EXAMPLE_DERIVED_DATA_PATH = '/'.join([DERIVED_DATA_PATH, 'example'])

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
  'FTS': 'Financial Tracking Service run by UN OCHA (via HDX)'
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

# HDX expected update frequency keywords (required for each Dataset)
HDX_UPDATE_FREQUENCY = [
  'Every day',
  'Every week',
  'Every two weeks',
  'Every month',
  'Every three months',
  'Every six months',
  'Every year',
  'Never'
]
