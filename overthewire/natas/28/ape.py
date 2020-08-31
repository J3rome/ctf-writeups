import requests
import json
import urllib.parse

url = "http://natas28:JWwR438wkgTsNKBbcJoowyysdM82YjeF@natas28.natas.labs.overthewire.org/index.php"

query = "you"
for i in range(100):
	query = "a"*i
	r = requests.post(url, data={'query': query}, allow_redirects=False)
	encoded_query = urllib.parse.unquote(r.headers['Location']).split('query=')[1]
	#print(encoded_query)
	print(f"{i} -- {len(encoded_query)}")
