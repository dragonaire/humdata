# Constants

# TODO: don't hardcode this to local computer
RAW_DATA_PATH = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data/raw'
DERIVED_DATA_PATH = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data/derived'

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
  'HNO': 'UN OCHA Humanitarian Needs Overview 2017',
  'DTM': 'IOM, NEMA, SEMA, Red Cross: Displacement Tracking Matrix, Round XIV Jan 2017',
  'ORS': 'Online Reporting System run by UN OCHA ROWCA (via HDX)'
}

# HDX data
HDX_DATASETS = [
  'lcb-displaced', 
  'lake-chad-basin-fts-appeal-data', 
  'lake-chad-basin-key-figures-january-2017'  # multiple resources
  #'conflict-events',
  #'lake-chad-basin-baseline-population'
  # lac-chad-basin-area (zipped shapefiles)
]

# Map of Dataset names to downoaded Resource files via HD
# Note: this is just for reference, e.g. to fall back on loading locally i the HDX API is unresponsive
HDX_RESOURCES = {
  'lcb-displaced': 'LCB_SnapShot_DataSets_24Jan17.xlsx---key_figures.csv',
  'lake-chad-basin-fts-appeal-data': 'Lake_Chad_Basin_Appeal_Status_2016-08-31.csv', 
  'lake-chad-basin-key-figures-january-2017': 'Lake_Chad_Basin_Displaced_2016-08-31.csv'
}

