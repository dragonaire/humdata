# Humdata
A humanitarian data service. 
The aspirational goal is to consolidate the various fragmented raw data sources, whether it be APIs, libraries, raw urls, or PDFs, behind a single REST API and expos via Swagger UI.
This is the initial effort to lay the groundwork for this to be possible.

# Preliminary TODOs (by 3/10)
- [x] install all dependencies and track them in reqs.txt files (e.g. swagger)
- [x] use hdx api to download, parse, and merge some data (first focus on lake chad basin)
- [x] lay out structure
- [x] lay out skeleton for rest api and swagger ui
- [x] add landing page with links to api docs and repo
- [x] construct endpoints for accessing the data
- [x] a single data source end to end
- [x] a set of lake chad basin data sources end to end (more granular than country level, or historic data)

# Swagger UI
See the [website](http://127.0.0.1:5000) with interactive API documentation [here](http://127.0.0.1:5000/apidocs/index.html). 
Note: this is currently local, to see it run the following:
```sh
python api.py
```
Current set of endpoints (for Lake Chad Basin, 2016-2017):
- GET /funding/totals/:country
- GET /funding/categories/:country
- GET /needs/totals/:country
- GET /needs/regions/:country

# Raw data sources
To pull data from HDX (the Humanitarian Data Exchange), run the following:
```sh
python3 run_hdx.py
```
This data script is configured to run every Monday at 2:30am (system time) for the latest data.
See `resources/constants.py` and `resources/data/raw`:
- [HDX Lake Chad Basin Key Figures January 2017](https://data.humdata.org/dataset/lake-chad-basin-key-figures-january-2017)
- [HDX Lake Chad Basin FTS Appeal Data](https://data.humdata.org/dataset/lake-chad-basin-fts-appeal-data)
- [HDX Lake Chad Basin Crisis Displaced Persons](https://data.humdata.org/dataset/lcb-displaced)
- [Lake Chad Basin Humanitarian Needs Overview January 2017](https://www.humanitarianresponse.info/system/files/documents/files/lcb_hnro_2017-en-final.pdf)
- [UNOCHA ORS ROWCA](http://ors.ocharowca.info/api/v2/KeyFigures/KeyFiguresLakeChad.ashx?country=4,8,9,3&subcat=9,10,4&datefrom=01-01-2016&dateto=21-02-2017&inclids=yes&final=1&format=json&lng=en)

# Derived data sources
See `resources/data/derived` - this cleaned and formatted data is what the API is ultimately serving.
