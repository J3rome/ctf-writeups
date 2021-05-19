import os

key = 'AdsipPewFlfkmll'
key_len = len(key)

to_decode = ['todo.html', 'index.html', 'reallyimportant.txt']

for file in to_decode:
	encoded_text = open(file, 'r').read()

	recovered = ""
	for i, c in enumerate(encoded_text):
		recovered += chr(ord(c) ^ ord(key[i % key_len]))

	os.rename(file, file + ".encrypted")

	with open(file, 'w') as f:
		f.write(recovered)

print("done")