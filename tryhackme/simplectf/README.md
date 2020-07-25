# Tryhackme.com Room : Simple CTF
`https://tryhackme.com/room/easyctf`


# Instance
```
export IP=10.10.214.243
```

# Task 1

1. How many services are running under port 1000?

Nmap scan result :
```
PORT     STATE SERVICE VERSION
21/tcp   open  ftp     vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
| FTP server status:
|      Connected to ::ffff:10.1.122.133
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 5
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp   open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 2 disallowed entries 
|_/ /openemr-5_0_1_3 
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
2222/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
```

```
2
```

2. What is running on the higher port?
```
ssh (Port 2222)
```

3. What's the CVE you're using against the application?
Originally looked up for ftp & ssh vulnerabilities. Didn't find anything.

There is a webserver running on port 80. Default installation page.

/robots.txt contains `Disallow: /openemr-5_0_1_3 ` But this directory is 404. Dead end.

Running gobuster on the web server : `gobuster dir -w /usr/share/dirb/wordlists/big.txt -u http://$IP`

GoBuster found this :
```
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/robots.txt (Status: 200)
/server-status (Status: 403)
/simple (Status: 301)
```

/simple is a CMS -- "CMS Made Simple 2.2.8"

Vulnerable to 
```
CVE-2019-9053
```

4. To what kind of vulnerability is the application vulnerable?
```
sqli
```

5. What's the password?






