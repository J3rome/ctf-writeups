# Tartagus

## User Flag

## Root Flag

## IP

```
export IP="10.10.230.213"
```

## Nmap Scan

```
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_-rw-r--r--    1 ftp      ftp            17 Jul 05 21:45 test.txt
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.143.183
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 1
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 98:6c:7f:49:db:54:cb:36:6d:d5:ff:75:42:4c:a7:e0 (RSA)
|   256 0c:7b:1a:9c:ed:4b:29:f5:3e:be:1c:9a:e4:4c:07:2c (ECDSA)
|_  256 50:09:9f:c0:67:3e:89:93:b0:c9:85:f1:93:89:50:68 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
MAC Address: 02:C0:8F:AD:40:CF (Unknown)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

## Ftp
test.txt :
```
vsftpd test file
```

## Http server

robots.txt :
```
User-Agent: *
Disallow : /admin-dir

I told d4rckh we should hide our things deep.
```

Potential username
```
d4rckh
```


Login page at `/sUp3r-s3cr3t`

We bruteforce the login and get 
```
enox:P@ssword1234
```

We get an upload page

The uploaded files go to
```
/sUp3r-s3cr3t/images/uploads/
```


User with login shell
```
root:x:0:0:root:/root:/bin/bash
vagrant:x:1000:1000:,,,:/home/vagrant:/bin/bash
thirtytwo:x:1004:1004::/home/thirtytwo:/bin/bash
d4rckh:x:1005:1005::/home/d4rckh:/bin/bash
```


/home/thirtytwo/note.txt
```
Hey 32, the other day you were unable to clone my github repository. 
Now you can use git. Took a while to fix it but now its good :)

~D4rckh
```

User flag in `/home/d4rckh/user.txt`:
```
0f7dbb2243e692e3ad222bc4eff8521f
```

root flag
```
7e055812184a5fa5109d5db5c7eda7cd
```



























