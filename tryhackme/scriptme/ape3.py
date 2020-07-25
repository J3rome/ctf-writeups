import socket
import time
import binascii
import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

ip = "10.10.84.246"
port = 4000

def send_msg(message, ip, port):
	sock.sendto(bytes(message, "utf-8"), (ip, port)) 
	return sock.recv(1024)

# Taken from PyCA doc
def decrypt(key, iv, ciphertext, tag):
    decryptor = Cipher(
        algorithms.AES(key),
        modes.GCM(iv, tag),
        backend=default_backend()
    ).decryptor()

    return decryptor.update(ciphertext) + decryptor.finalize()


sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
print(send_msg('hello', ip, port))
print(send_msg('ready', ip, port))

to_decrypt = []
tags = []
count = 0

while True:
	tag = send_msg('final', ip, port)

	if tag in to_decrypt:
		break

	if len(tag) == 16:
		print(f"Tag : {binascii.hexlify(tag)}")
		tags.append(tag)
	else:
		print(f"to_decrypt : {binascii.hexlify(tag)}")
		to_decrypt.append(tag)

	count += 1

	time.sleep(0.1)

print(f"Tag repeated after {count}")

key = b"thisisaverysecretkeyl337"
iv = b"secureivl337"
valid_checksum = "5d77f018d2bf777860548655d84d7382dc27d6ce816ede68f65d72621463d9da"
for encrypted, tag in zip(to_decrypt, tags):

	decrypted = decrypt(key, iv, encrypted, tag)
	decrypted_hash = hashlib.sha256(decrypted).hexdigest()

	if decrypted_hash == valid_checksum:
		print("\n=============================")
		print("This is the flag : ")

	print(f"Decrypted : {decrypted} -- Hash : {decrypted_hash}")

	if decrypted_hash == valid_checksum:
		print("=============================\n")
