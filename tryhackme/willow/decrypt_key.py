with open('key.encrypted', 'r') as f:
	to_decrypt = f.read().strip().split(" ")

e = 23
d = 61527
n = 37627

decrypted = ""
for c in to_decrypt:
	decrypted += chr(int(c) ** d % n)
	print(decrypted)

print("\n\n DECRYPTION FINISHED \n\n")
print(decrypted)

with open('key.decrypted', 'w') as f:
	f.write(decrypted)
