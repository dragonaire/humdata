# Humdata
A humanitarian data service. 
The aspirational goal is to consolidate the various fragmented raw data sources, whether it be APIs, libraries, raw urls, or PDFs, behind a single REST API.
This is the initial effort to lay the groundwork for this to be possible.

# Preliminary TODOs (by 3/10)
- [x] install all dependencies and track them in reqs.txt files (e.g. swagger)
- [x] use hdx api to download, parse, and merge some data (first focus on lake chad basin)
- [x] lay out structure
- [ ] lay out skeleton for rest api and swagger ui
- [ ] set up database and initial schemas
- [ ] scripts to load data into database
- [ ] construct endpoints for accessing the data
- [ ] a single data source end to end
- [ ] a set of lake chad basin data sources end to end (allow for merges/joins)

# Raw data sources
See `resources/constants.py` and `resources/data/raw`:
- [HDX Lake Chad Basin Key Figures January 2017](https://data.humdata.org/dataset/lake-chad-basin-key-figures-january-2017)
- [HDX Lake Chad Basin FTS Appeal Data](https://data.humdata.org/dataset/lake-chad-basin-fts-appeal-data)
- [HDX Lake Chad Basin Crisis Displaced Persons](https://data.humdata.org/dataset/lcb-displaced)
- [Lake Chad Basin Humanitarian Needs Overview January 2017](https://www.humanitarianresponse.info/system/files/documents/files/lcb_hnro_2017-en-final.pdf)
- [UNOCHA ORS ROWCA](http://ors.ocharowca.info/api/v2/KeyFigures/KeyFiguresLakeChad.ashx?country=4,8,9,3&subcat=9,10,4&datefrom=01-01-2016&dateto=21-02-2017&inclids=yes&final=1&format=json&lng=en)

