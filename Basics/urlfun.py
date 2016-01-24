import urllib.request as urlreq
import urllib.parse as urlparse

url = "https://www.google.co.uk/?gws_rd=ssl&"
values = {'q': 'python programming tutorials'}

query = urlparse.urlencode(values)
url = url + query

# Spoof a Mozilla search engine
headers = dict()
headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686)"

req = urlreq.Request(url, headers=headers)
resp = urlreq.urlopen(req)
print(resp.read())

