# HTML-Scrapper
HTML scraper
Author: Nielson Janné
License: MIT

fetches company data/emails from:
https://www.defysiotherapeut.com

Data can be requested through REST API at:
/restservices/portfolio

note: The REST API returns the first 100 entries regardless of actual query result.

Search parameters REST API accepts:
    postalcode
    maxdistance (dosn't work propperly within the API)
    city
    therapist
    fysiotype
    practice

parameters should be in Dutch language/names