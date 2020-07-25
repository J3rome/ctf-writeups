
# Tryhackme.com Room : ConvertMyVideo
`https://tryhackme.com/room/convertmyvideo`


# Task 1

1. This file has been base64 encoded 50 times - write a script to retrieve the flag. Here is the general process to do this:

We write this :
```
#!/bin/bash

TO_DECODE="$(cat tsk1_base64_50times.txt)"

for i in {1..50};do
	TO_DECODE="$(echo ${TO_DECODE} | base64 -d)"
done

echo ${TO_DECODE}
```

And we find
```
HackBack2019=
```

# Task 2

```
You need to write a script that connects to this webserver on the correct port, do an operation on a number and then move onto the next port. Start your original number at 0.

The format is: operation, number, next port.

For example the website might display, add 900 3212 which would be: add 900 and move onto port 3212.

Then if it was minus 212 3499, you'd minus 212 (from the previous number which was 900) and move onto the next port 3499

Do this until you the page response is STOP (or you hit port 9765).

Each port is also only live for 4 seconds. After that it goes to the next port. You might have to wait until port 1337 becomes live again...

Go to: http://<machines_ip>:3010 to start...
```

# Instance
```
export IP=10.10.56.89
```

We write the following python script to solve the challenge :
```py
import sys
import requests
import time

def get_initial_port(ip):
	# Quick and dirty parsing
	r = requests.get(f'http://{ip}:3010')
	t = r.text.split('id="onPort">')[1]
	t = t.split("</a>")[0]
	return int(t)

ip = "10.10.56.89"
print("Waiting for port 1337...")

port = get_initial_port(ip)
while port != 1337:
	port = get_initial_port(ip)
	time.sleep(3)

print(f"Starting...")

current = 0
while True:
	try:
		r = requests.get(f"http://{ip}:{port}")
	except:
		# We just hammer the server while waiting to the port to open
		continue

	splitted = r.text.split(' ')

	if len(splitted) != 3 or port == 9765:
		print(r.text)
		print(f"Current number : {current}")
		exit(0)

	last_port = port
	operation, val, port = splitted

	print(f"Current Value: {current}")
	print(f"Operation : {operation} -- Operande : {val}")
	print(f"Port : {last_port} -> {port}")

	val = float(val)

	if operation == "add":
		current += val
	elif operation == "minus":
		current -= val
	elif operation == "multiply":
		current *= val
	elif operation == "divide":
		current /= val
	else:
		print(f"Unknown operation : {operation}")
		exit(0)

	time.sleep(2)

```

The answer is 
```
344769.12
```

# Task 3 [Hard] Encrypted Server Chit Chat

```
The VM you have to connect to has a UDP server running on port 4000. Once connected to this UDP server, send a UDP message with the payload "hello" to receive more information. You will find some sort of encryption(using the AES-GCM cipher). Using the information from the server, write a script to retrieve the flag.
```

# Instance
```
export IP=10.10.193.219
```

We send the `hello` command to the server on port `4000` and receive:
```
b"You've connected to the super secret server, send a packet with the payload ready to receive more information"
```

We send `ready` and receive :
```
key:thisisaverysecretkeyl337 
iv:secureivl337 
to decrypt and find the flag that has a SHA256 checksum of ]w\xf0\x18\xd2\xbfwx`T\x86U\xd8Ms\x82\xdc'\xd6\xce\x81n\xdeh\xf6]rb\x14c\xd9\xda send final in the next payload to receive all the encrypted flags"
```

SHA256 Checksum:
```
5d77f018d2bf777860548655d84d7382dc27d6ce816ede68f65d72621463d9da
```
Seems like hex and characters are mixed together...

Seems like I'm overthinking again/not reading correctly.. just need to send `final` and we receive :
```
b'h\t: \xe9\xa1\x98\xbd\xa4\x1f 9F \xdd\x1d'
```

Sending `final` again give us another 16 bytes of data.
The data repeat after `32` times.
We actually don't get 16 bytes every time. We get :
```
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 13 bytes
received 16 bytes
received 28 bytes
received 16 bytes
Tag repeated after 32
```

Ok soo, after poking around this for way too long. I figured that the first message is the `encrypted payload` (13 bytes) and the second message (16 bytes) is the `tag` .
All of this was actually written in the task details.. Didn't get that while reading it...

Now we just need to use the secret key, the iv and the appropriate tags to decrypt the messages with PyCA.
```
key = thisisaverysecretkeyl337 
iv = secureivl337 
```

Running our script we get :
```
Decrypted : b'THM{SRBOKB2N}' -- Hash : b880605ddf97b71bd7ddebe53cd96b26facc3daf2fe8952e4010e4782114d6ba
Decrypted : b'THM{LPDBVV5X}' -- Hash : cb78b079e56c97c444a284b0215e05ce0158e39d97f8ba359c572c6cd2782401
Decrypted : b'THM{4EB5WRZ0}' -- Hash : 5618e3ac354e82cb889c7ff7c7a55909366fbb5f25cb752994ff694c339ee25c
Decrypted : b'THM{VQPDTAZ7}' -- Hash : 2e9634815e4400d91ba6fc2afb7af4c64c9176a5dfe89aa39ce8744c9fef7be0
Decrypted : b'THM{IGF8G7WY}' -- Hash : 2567453f754f143618b65f3bce32837062852ec0a7f4741462cc924ffcc4299a
Decrypted : b'THM{DSW48SJG}' -- Hash : 65007d0bfe29497f2e3f57218b1b5a3f1cff27c2305258d19741822402b809e1
Decrypted : b'THM{OP7JMOZL}' -- Hash : 11201911cb67d18d424c26cd1718137154d6f3eaaead971a6c6f81a700b9d4df
Decrypted : b'THM{YIY2XCPY}' -- Hash : f53d9155c8f6b6bb7ff40fdc23f9c36f5e62d75970cc00223a0bdb2e00ea6382
Decrypted : b'THM{ZNYB9HRZ}' -- Hash : 17da28543c9863cb230f5021f5f946d272b508e78b1b04208ab11ce24a0fb563
Decrypted : b'THM{QMT2WD8J}' -- Hash : c3b7e65af4eccaa11432e624efeecc79c31e3b31a69066111a38e5855bc81ef7
Decrypted : b'THM{8UUBSSV8}' -- Hash : f4b20b78ac6cbdfb7dcd089d2299d39b69727c375cacc4b9117e3059b1f4cfd8

=============================
This is the flag : 
Decrypted : b'THM{eW-sCrIpTiNg-AnD-cRyPtO}' -- Hash : 5d77f018d2bf777860548655d84d7382dc27d6ce816ede68f65d72621463d9da
=============================

Decrypted : b'THM{HF6RVIOZ}' -- Hash : b3da4795575b9a5eedde8c6ad3cd4464de6ccc9577697c7e8e7b919ef01d1953
Decrypted : b'THM{2XMB773B}' -- Hash : 0eb977b88fdbca9402eeae3ffe76cecb9f54f9a7d30ac2205fc7a1c15ca1417c
Decrypted : b'THM{ZFW2PDZX}' -- Hash : 5c68218f511c35773a570917e0e0ca9ed29e50e01c434c8070d58676137f5af4
Decrypted : b'THM{TOK527ZZ}' -- Hash : 155194be92be972fb8380e93f88d056fa37891c9cc51d60ef5322a508dbb6d2c
```

We decrypt all the messages and find the flag in the 24 bytes message :
```
THM{eW-sCrIpTiNg-AnD-cRyPtO}
```

Here is the script :
```py
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

```
