"""
db_populate.py
Uses very basic web scraping and file stripping to populate a
database of names and addresses. MongoDB is used as the NoSQL/document database foundation
db = customers

collections:
first_names - a collection of popular male and female first names (from the US)
surnames - a collection of the 2000 most common US surnames (c.2003)
towns - a listing of towns against counties in the UK

all collections are indexed to allow for a random selection algorithm
"""

from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
import pymongo as mgo


# Create a wrapper function for urlopen
def open_url(target_url):
    try:
        page = urlopen(target_url)
    except HTTPError as err:
        print("open_url:", err)
        return None
    except URLError as err:
        print("open_url: The url '{}' could not be found.".format(target_url), err)
        return None
    else:
        return page


# An example of web scraping
# targets various tables from the website "http://names.mongabay.com/"
def process_name_pages(target_url, table_name):
    headers = dict()
    headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686)"
    req = Request(url, headers=headers)
    print("Requesting data from URL:'{}'".format(target_url))
    http = open_url(req)
    page = BeautifulSoup(http, 'lxml')

    names = []
    for tr in page.find('table', {"id": table_name}).tr.next_siblings:
        for element in tr:
            if not isinstance(element, str):
                name = str(element)
                if name.startswith('<td>'):
                    name = name[4:-5].capitalize()
                    names.append(name)
                    break
    return names


# An example of a stripped web page: target page produced alt page if scraping was attempted
# so this works directly on a local copy of the source code
def process_town_pages():
    towncounty = []
    count = 0
    with open('towncounty.html', 'r') as fd:
        for line in fd:
            if line.startswith('<tr><td class="r">'):
                count += 1
                line = line.strip()
                line = line[len('<tr><td class="r">'):-(len('</td></tr>'))]
                town, county = line.split('</td><td>')
                towncounty.append((count, town, county))
    return towncounty

if __name__ == '__main__':
    # Web scraping
    url = "http://names.mongabay.com/data/1000.html"
    surnames1 = process_name_pages(url, "myTable")
    url = "http://names.mongabay.com/data/2000.html"
    surnames2 = process_name_pages(url, "myTable")
    surnames = surnames1 + surnames2
    surnames = enumerate(surnames, 1)
    url = "http://names.mongabay.com/male_names_alpha.htm"
    male_first_names = process_name_pages(url, "myTable")
    url = "http://names.mongabay.com/female_names_alpha.htm"
    female_first_names = process_name_pages(url, "myTable")
    first_names = male_first_names + female_first_names
    first_names.sort()
    first_names = enumerate(first_names, 1)
    town_county = process_town_pages()

    # Populating the database
    print("Connecting to mongoDB...")

    with mgo.MongoClient('mongodb://localhost:27017/') as client:
        db = client['random_names']
        fname = db.create_collection('first_names')
        sname = db.create_collection('surnames')
        print("Inserting first name data into 'random_names.first_names'...")
        fname.insert_many([{"name": name, "number": count} for count, name in first_names])
        print("Inserting surname data into 'random_names.surnames'...")
        sname.insert_many([{"last_name": name, "number": count} for count, name in surnames])

        # Change the cursor target
        db = client['uk_towns']
        print("Inserting town/county data into 'uk.towns.town_and_county'...")
        tcount = db.create_collection('town_and_county')
        tcount.insert_many([{"number": number, "town": town, "county": county} for number, town, county in town_county])
        print("Closing client connection")
