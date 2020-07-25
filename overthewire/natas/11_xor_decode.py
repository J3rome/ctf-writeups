import base64
import json
import requests

def do_xor(to_encode, key):
	out = []
	for i, word in enumerate(to_encode):
		out.append(ord(word) ^ ord(key[i % len(key)]))

	return "".join([chr(o) for o in out])

def retrieve_key_from_potential(potential_key):
	# This will extract the key when presented a string with the format "keykeykeykeykey"
	# Will take the first repeating pattern. Pattern must start at the beginning of the string
	current = ""

	for i, letter in enumerate(potential_key):
		current += letter

		next_word = potential_key[i+1:i + 1 + len(current)]

		if current == next_word :
			return current

	return None

url = "http://natas11:U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK@natas11.natas.labs.overthewire.org"

cookie = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw="
# php json encode result in a string without any space while python json.dumps add spaces. We must specify separators
content = json.dumps({'showpassword':'no', 'bgcolor':"#ffffff"}, separators=(',', ":"))

to_decode = base64.b64decode(bytes(cookie, 'utf-8')).decode('utf-8')

potential_key = do_xor(to_decode, content)

key = retrieve_key_from_potential(potential_key)

new_cookie = do_xor(json.dumps({'showpassword': 'yes', 'bgcolor': '#ffffff'}), key)
new_cookie = base64.b64encode(bytes(new_cookie, 'utf-8')).decode('utf8')

r = requests.get(url, cookies={'data': new_cookie})

next_password = r.text.split('The password for natas12 is ')[1].split('<br>')[0]

print(f"Natas12 password is {next_password}")
