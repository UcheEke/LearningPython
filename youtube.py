import json
from urllib.request import urlopen
url = "https://gdata.youtube.com/feeds/api/standardfeeds/top_rated?alt=json"

response = urlopen(url)
print("Response:\n\n", response)

contents = response.read()
print("Contents:\n\n", contents)

text = contents.decode('utf8')
print("Text:\n\n",text)

data = json.loads(text)
print("Data:\n\n", data)

print("\n\nTop ranked videos at the moment on YouTube:\n")
for video in data['feed']['entry'][0:6]:
	print(video['title']['$t'])
