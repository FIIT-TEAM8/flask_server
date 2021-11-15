# flask_server

# Search articles

Parameters:

* q - search query
* from - YYYY-MM-DD date, starting publishing date for articles returned by this request
* to - YYYY-MM-DD date, ending publishing date for articles returned by this request
* locale - locale of returned articles

Examples:
```
curl -X GET https://team08-21.studenti.fiit.stuba.sk/api/v1/search/?q=Marian+Kocner
```
```
curl -X GET https://team08-21.studenti.fiit.stuba.sk/api/v1/search/?q=Marian+Kocner&locale=en-gb&from=2020-01-01&to=2021-01-01
```
