import csv
import json
import urllib.request
import datetime

CSV_FILE_NAME = 'FysioData.csv'
TXT_FILE_NAME = 'FysioMails.txt'
URL = "https://www.defysiotherapeut.com/restservices/portfolio"


def Main():

    print("\nStart Data scraping from: \n" + URL + "\n")
    csvFile = open(CSV_FILE_NAME, 'w', encoding="utf-8")
    fields = ('Bedrijfsnaam', 'Plaats', 'Email', 'Website', 'Telefoonnummer')
    file_writter = csv.DictWriter(
        csvFile, fieldnames=fields, lineterminator='\n', quoting=csv.QUOTE_ALL)
    file_writter.writeheader()

    txtFile = open(TXT_FILE_NAME, "w")

    duplicates = set()  # Keep track of duplicates
    unique = 0

    for x in range(20, 201):
        postalcode = str(x * 50) + 'AA'
        querystring = "?postalcode=" + postalcode + "&maxdistance=50"
        data = scrapeAPI(URL, querystring)
        unique = processData(txtFile, file_writter, data, duplicates, unique)
        time = datetime.datetime.now().strftime("%H:%M:%S")
        print(f"[ {time} ] [ Postalcode: {postalcode} ] [ added: {unique:4} ]")

    csvFile.close()
    txtFile.close()
    print("\n-----------------")
    print("scraping complete\n")
    print("Company data saved to: " + CSV_FILE_NAME)
    print("Emails saved to:" + TXT_FILE_NAME)
    print()


def scrapeAPI(url, querystring):
    jsondata = urllib.request.urlopen(url + querystring)
    data = json.loads(jsondata.read())
    jsondata.close()
    urllib.request.urlcleanup()
    return data


def processData(txtFile, csvWritter, data, duplicates, unique):
    for datapoint in data:
        company = datapoint['naam']
        # API contains duplicates with different cases.
        email = datapoint['email'].lower()
        website = datapoint['website']
        location = datapoint['plaats']
        phonenumber = datapoint['telefoon']
        if email == '':
            continue
        if email in duplicates:
            continue
        unique += 1
        duplicates.add(email)
        csvWritter.writerow({
            'Bedrijfsnaam': company,
            'Plaats': location,
            'Email': email,
            'Website': website,
            'Telefoonnummer': phonenumber
        })
        txtFile.write(email + "\n")
    return unique


if __name__ == "__main__":
    Main()
