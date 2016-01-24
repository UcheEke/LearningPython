from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup


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

html = openURL("http://www.pythonscraping.com/pages/page3.html")
page = BeautifulSoup(html, "lxml")

query = page.find("table", {"id": "giftList"})

try:
    for descendant in query.descendants:
        print(descendant)
except AttributeError as e:
    print("query not executable:\n{}".format(e))
