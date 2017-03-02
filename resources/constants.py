# Constants

HDX_DATASETS = [
  'lcb-displaced', 
  'lake-chad-basin-fts-appeal-data', 
  'lake-chad-basin-key-figures-january-2017'  # multiple resources
  #'conflict-events',
  #'lake-chad-basin-baseline-population'
  # lac-chad-basin-area (zipped shapefiles)
]


# TODO: don't hardcode this to local computer
DATA_DOWNLOAD_PATH = '/Users/yang/Documents/clients/onecampaign/project/humdata/resources/data'

# Map of country codes to country names, ISO 3166-1 alpha-3 (similar to UNDP and NATO standards)
country_codes = {
  'CHD': 'Chad',
  'CMR': 'Cameroon',
  'NER': 'Niger',
  'NGR': 'Nigeria'
}

# Map of Dataset names to downoaded Resource files (via HDX)
resources = {
  'lcb-displaced': 'LCB_SnapShot_DataSets_24Jan17.xlsx---key_figures.csv',
  'lake-chad-basin-fts-appeal-data': 'Lake_Chad_Basin_Appeal_Status_2016-08-31.csv', 
  'lake-chad-basin-key-figures-january-2017': 'Lake_Chad_Basin_Displaced_2016-08-31.csv'
}

