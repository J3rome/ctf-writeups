# Tryhackme.com Room : Inferno

`https://tryhackme.com/room/inferno

## Instance

```bash
export IP="10.10.220.36"
```

## Nmap

```
21/tcp    open  tcpwrapped
22/tcp    open  ssh           OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 d7:ec:1a:7f:62:74:da:29:64:b3:ce:1e:e2:68:04:f7 (RSA)
|   256 de:4f:ee:fa:86:2e:fb:bd:4c:dc:f9:67:73:02:84:34 (ECDSA)
|_  256 e2:6d:8d:e1:a8:d0:bd:97:cb:9a:bc:03:c3:f8:d8:85 (ED25519)
23/tcp    open  tcpwrapped
25/tcp    open  tcpwrapped
|_smtp-commands: Couldn't establish connection on port 25
80/tcp    open  http          Apache httpd 2.4.29 ((Ubuntu))
| http-methods: 
|_  Supported Methods: POST OPTIONS HEAD GET
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Dante's Inferno
88/tcp    open  tcpwrapped
106/tcp   open  pop3pw?
110/tcp   open  tcpwrapped
389/tcp   open  tcpwrapped
443/tcp   open  tcpwrapped
464/tcp   open  tcpwrapped
636/tcp   open  tcpwrapped
777/tcp   open  tcpwrapped
783/tcp   open  tcpwrapped
808/tcp   open  ccproxy-http?
873/tcp   open  tcpwrapped
1001/tcp  open  webpush?
1236/tcp  open  tcpwrapped
1300/tcp  open  tcpwrapped
2000/tcp  open  tcpwrapped
2003/tcp  open  tcpwrapped
2121/tcp  open  tcpwrapped
2601/tcp  open  tcpwrapped
2602/tcp  open  tcpwrapped
2604/tcp  open  tcpwrapped
2605/tcp  open  tcpwrapped
2607/tcp  open  tcpwrapped
2608/tcp  open  tcpwrapped
4224/tcp  open  tcpwrapped
5051/tcp  open  tcpwrapped
5432/tcp  open  tcpwrapped
5555/tcp  open  tcpwrapped
5666/tcp  open  tcpwrapped
6346/tcp  open  tcpwrapped
6566/tcp  open  tcpwrapped
6667/tcp  open  tcpwrapped
|_irc-info: Unable to open connection
8021/tcp  open  tcpwrapped
8081/tcp  open  tcpwrapped
8088/tcp  open  radan-http?
9418/tcp  open  tcpwrapped
10000/tcp open  tcpwrapped
10082/tcp open  tcpwrapped
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

Lot's of ports opened. Scanning all ports while looking around.



The website on port `80` is just a static html with an image and an italian quote.

gobuster didn't find anything usefull so far...



Hmm, seems like we will have to check all those ports.

Tried to connect ot a bunch of them but they don't seem to answer anything..

Written a python script to test all ports but none of them seems to answer anything.. Maybe we are not sending the correct payload for the port to activate ?



gobuster returned with the page `/inferno` which is protected by htaccess file so we need a username and password.



Sooo, after looking around, I looked at a writeup for hints and well, we just need to bruteforce the login. So let's do that.

I first tried to do it with `patator` but it was super slow..

Using `hydra` we found the password pretty easily.

```
admin:dante1
```

We are greeted with a login form. The same credentials works.



We not have access to some kind  online IDE.

We can browse some files in a git repo.



Seems like this is the code of the actual IDE ?

Yep, looking at the `config.php` file we see 

```php
define("BASE_PATH", "/var/www/html/inferno");
```

So we can most probably inject some code in there.

Well, actually, we can't. We can't modify anything.



Found an exploit on the web `https://github.com/WangYihang/Codiad-Remote-Code-Execute-Exploit/blob/master/exploit.py`

Had to modify it a bit, there was an error in a url path (Was getting a 404 for some call).



Now we are in as `www-data`, the session get killed every minutes or so.

I'm pretty sure this is because of `/var/www/html/machine_services1320.sh` which create a bunch of `nc` listener on a bunch of port.

It also does a `pkill bash` which kill our session.

By spawning a pty via python we at least get a chance to respawn another process before getting kicked out of the server.

Also, calling `sh` allows us to keep our session running indefinetly but it's a shitty shell..

We can just create a symlink to `bash` with a different name.

This will allow us to evade the `pkill bash` statement and have autocomplete, etc



After a while, i decided to run `linpeas` but it didn't find much.



Oh well, it was something i looked at quickly but overlooked.

There is a file named `/home/dante/Downloads/.download.dat` containing a bunch of hex encoded string.



It's part of an italian poem and at the end we have :

```
dante:V1rg1l10h3lpm3
```

Which are the credential for the user `dante`

`/home/dante/local.txt` :

```
77f6f3c544ec0811e2d1243e2e0d1835
```



## Priv esc

Once logged as `dante` we have the same problem as before, our bash shell get killed.

Again we create a symlink to bash with another name and run it.

Maybe this wouldn't happen if we were logged in via `ssh` ?



Anyhow

When running `sudo -l` we get 

```
User dante may run the following commands on Inferno:
    (root) NOPASSWD: /usr/bin/tee
```



Interesting, we can write stuf anywhere with `tee`



We can add ourselves to `/etc/sudoers` file using

```bash
echo 'dante ALL=(ALL) NOPASSWD: ALL' | sudo /usr/bin/tee -a /etc/sudoers
```

And we can now `sudo bash` and we are root !



`/root/proof.txt` :

```
f332678ed0d0767d7434b8516a7c6144
```



## Follow up

This took me way longer than needed.

* First, I didn't think I would need to bruteforce the login, I was looking for some other clues, looking at the opened ports.
* Second, didn't investigate enough why the exploit script was not working.. I just blindly runned it and assumed the server was not vulnerable when it didn't work..
  * When I took a look at the endpoint it was trying to reach, the problem was obvious (missing `/`) so i fixed it and got the shell.
* Finally, I overlooked the `.download.dat` file. Should have known better and investigated more.
  * Should have looked at the `docx` also, even tho they were not useful. Should always look at everything !

## End



