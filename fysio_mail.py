"""
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
"""
import csv
import json
import urllib.request

CSV_FILE_NAME = 'FysioMails.csv'

CITIES = ["Delft", "Rotterdam", "Amsterdam", "Leiden", "Dordrecht", "Maastricht", "Groningen",
          "Utrecht", "Eindhoven", "Leeuwarden", "Alkmaar", "Middelburg", "Enschede", "Tilburg",
          "Zwolle", "Emmen", "Sneek", "Roermond", "Venlo", "Amersfoort", "Almere", "Gouda",
          "Lelystad", "Apeldoorn", "Haarlem", "Zoetermeer", "'S-Hertogenbosch", "Breda", "Nijmegen",
          "'S-Gravenhage"]

LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
           'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']


def Main():
    print("Start Data scraping from https://www.defysiotherapeut.com")
    file = open(CSV_FILE_NAME, 'w', encoding="utf-8")
    fields = ('Bedrijfsnaam', 'Plaats', 'Email', 'Website', 'Telefoonnummer')
    file_writter = csv.DictWriter(
        file, fieldnames=fields, lineterminator='\n', quoting=csv.QUOTE_ALL)
    file_writter.writeheader()

    duplicates = set()   # set with unique emails
    dupcounter = 0
    unique = 0

    for city in CITIES:
        data = scrapeAPI(
            "https://www.defysiotherapeut.com/restservices/portfolio?city=", city)
        processData(file_writter, data, duplicates, dupcounter, unique)
        print("complete: " + city + "\t : " + str(unique) +
              " total\t" + str(dupcounter) + " dups")

    file.close()  # clean up CSV file
    print("------------------")
    print("scraping complete:")
    print("Total: " + str(unique))


def scrapeAPI(url, city):
    # fetch data from Rest API
    jsondata = urllib.request.urlopen(url
                                      + city)
    data = json.loads(jsondata.read())
    # clean up
    jsondata.close()
    urllib.request.urlcleanup()
    return data


def processData(file_writter, data, duplicates, dupcounter, unique):
    # process and write data
    for datapoint in data:
        company = datapoint['naam']
        # lowercase all emails, API DB does contain duplicate emails because it's case sensitive and they program like shit.
        email = datapoint['email'].lower()
        website = datapoint['website']
        location = datapoint['plaats']
        phonenumber = datapoint['telefoon']

        # preform checks
        if email == '':
            continue
        if email in duplicates:
            dupcounter += 1
            continue

        # write unique email to file
        unique += 1
        duplicates.add(email)
        file_writter.writerow({'Bedrijfsnaam': company, 'Plaats': location,
                               'Email': email, 'Website': website, 'Telefoonnummer': phonenumber})


if __name__ == "__main__":
    Main()
