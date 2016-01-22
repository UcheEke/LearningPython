from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pymongo as mgo


# Create a wrapper function for urlopen
def openURL(url):
    try:
        page = urlopen(url)
    except HTTPError as err:
        print("openURL:", err)
        return None
    except URLError as err:
        print("The url '{}' could not be found.", err)
        return None
    else:
        return page


# An example of web scraping
def processNamesPage(url, tableName):
    headers = dict()
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686)"
    req = Request(url, headers=headers)
    print("Requesting data from URL:'{}'".format(url))
    http = openURL(req)
    page = BeautifulSoup(http, 'lxml')

    names = []
    for tr in page.find('table', {"id": tableName}).tr.next_siblings:
        for element in tr:
            if not isinstance(element, str):
                name = str(element)
                if name.startswith('<td>'):
                    name = name[4:-5].capitalize()
                    names.append(name)
                    break
    return names


# An example of a stripped webpage
def processTownPages():
    townCounty = []
    count = 0
    with open('towncounty.html', 'r') as fd:
        for line in fd:
            if line.startswith('<tr><td class="r">'):
                count += 1
                line = line.strip()
                line = line[len('<tr><td class="r">'):-(len('</td></tr>'))]
                town, county = line.split('</td><td>')
                townCounty.append((count, town, county))
    return townCounty



if __name__ == '__main__':
    # Web scraping
    url = "http://names.mongabay.com/data/1000.html"
    surnames1 = processNamesPage(url, "myTable")
    url = "http://names.mongabay.com/data/2000.html"
    surnames2 = processNamesPage(url, "myTable")
    surnames = surnames1 + surnames2
    surnames = enumerate(surnames, 1)
    url = "http://names.mongabay.com/male_names_alpha.htm"
    male_firstnames = processNamesPage(url, "table1")
    url = "http://names.mongabay.com/female_names_alpha.htm"
    female_firstnames = processNamesPage(url, "table1")
    firstnames = male_firstnames + female_firstnames
    firstnames.sort()
    firstnames = enumerate(firstnames, 1)
    townCounty = processTownPages()

    print("Connecting to mongoDB...")

    with mgo.MongoClient('mongodb://localhost:27017/') as client:
        db = client['customers']
        fname = db.create_collection('firstnames')
        sname = db.create_collection('surnames')
        tcount = db.create_collection('towns')
        print("Inserting firstname data into 'customers.firstnames'...")
        fname.insert_many([{"name": name, "number" : count} for count, name in firstnames])
        print("Inserting surname data into 'customers.surnames'...")
        sname.insert_many([{"lastname": name, "number": count} for count, name in surnames])
        print("Inserting town data into 'customers.towns")
        tcount.insert_many([{"number": number, "town": town, "county": county} for number, town, county in townCounty])
        print("Closing client connection")

