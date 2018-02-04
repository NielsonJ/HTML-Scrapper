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

CITIES = ["Delft", "Rotterdam", "Amsterdam", "Leiden", "Dordrecht", "Maastricht", "Groningen",
          "Utrecht", "Eindhoven", "Leeuwarden", "Alkmaar", "Middelburg", "Enschede", "Tilburg",
          "Zwolle", "Emmen", "Sneek", "Roermond", "Venlo", "Amersfoort", "Almere", "Gouda",
          "Lelystad", "Apeldoorn", "Haarlem", "Zoetermeer", "'S-Hertogenbosch", "Breda", "Nijmegen",
          "'S-Gravenhage"]

CSV_FILE_NAME = 'FysioMails.csv'

def main():
    # open csv file and write header
    print("Start Data scraping from https://www.defysiotherapeut.com")
    file = open(CSV_FILE_NAME, 'w', encoding="utf-8")
    fields = ('Bedrijfsnaam', 'Plaats', 'Email', 'Website', 'Telefoonnummer')
    file_writter = csv.DictWriter(file, fieldnames=fields, lineterminator='\n', quoting=csv.QUOTE_ALL)
    file_writter.writeheader()

    emaillist = set()   # set with unique emails
    duplicates = 0
    unqiue = 0

    for city in CITIES:
        # fetch data from Rest API
        jsondata = urllib.request.urlopen("https://www.defysiotherapeut.com/restservices/portfolio?city=" + city)
        data = json.loads(jsondata.read())
        # clean up
        jsondata.close()
        urllib.request.urlcleanup()

        # process and write data
        for datapoint in data:
            company = datapoint['naam']
            email = datapoint['email'].lower() # lowercase all emails, API DB does contain duplicate emails because it's case sensitive and they program like shit.
            website = datapoint['website']
            location = datapoint['plaats']
            phonenumber = datapoint['telefoon']

            # preform checks
            if email == '':
                continue
            if email in emaillist:
                duplicates += 1
                continue
            
            # write unique email to file
            unqiue += 1
            emaillist.add(email)
            file_writter.writerow({'Bedrijfsnaam':company, 'Plaats':location, 'Email':email, 'Website':website, 'Telefoonnummer':phonenumber})
        print("complete: " + city + "\t : " + str(unqiue) + " total\t" + str(duplicates) + " dups")

    file.close() # clean up CSV file
    print("------------------")
    print("scraping complete:")
    print("Total: " + str(unqiue))

if __name__ == "__main__":
    main()
