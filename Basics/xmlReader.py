#!/usr/bin/env python3

"""
Pulling data from an XML document

We're going to read from www.nationaljournal.com/politics?rss=1
Using Beautiful Soup 4

"""

from bs4 import BeautifulSoup
import urllib.request
from time import sleep

req = urllib.request.urlopen("http://www.nypl.org/news/feed")

# Read the xml
xml = BeautifulSoup(req, 'xml')

i = 0
links = dict()
for item in xml.findAll('link'):
    i += 1
    links[str(i)] = item.text
    print("{} - {}".format(i, item.text))

choice = input("Choose a title by number: ").strip()
link = links[choice]
print("Going to {}...".format(link))

page = BeautifulSoup(urllib.request.urlopen(link).read(), 'lxml')

for p in page.findAll('p'):
    print(p.text)

    sleep(10)

