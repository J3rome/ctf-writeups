import os

key = 'AdsipPewFlfkmll'.encode('utf-8')
key_len = len(key)

to_decode = ['todo.html', 'index.html', 'reallyimportant.txt']
to_decode = ['todo.html']

for file in to_decode:
	encoded_text = open(file, 'rb').read()

	recovered = bytearray()
	for i, c in enumerate(encoded_text):
		recovered.append(c ^ key[i % key_len])

	os.rename(file, file + ".encrypted")

	with open(file, 'wb') as f:
		f.write(recovered)

print("done")