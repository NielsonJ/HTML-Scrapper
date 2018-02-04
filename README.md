# HTML-Scrapper
HTML scraper
Author: Nielson Janné
License: MIT

fetches company data/emails from:
https://www.defysiotherapeut.com

Data can be requested through REST API at:
/restservices/portfolio

Known search parameters:
* postalcode
* maxdistance (dosn't work propperly within the API)
* city
* therapist
* fysiotype
* practice

note: 
* The REST API returns the first 100 entries regardless of actual query result.
* parameters should be in Dutch language/names.
