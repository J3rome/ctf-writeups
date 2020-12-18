# Tryhackme.com Room : NerdHerd
`https://tryhackme.com/room/nerdherd`


# Instance
```
export IP=10.10.42.21
```

# Nmap
```
21/tcp  open  ftp         vsftpd 3.0.3
| ftp-anon: Anonymous FTP login allowed (FTP code 230)
|_drwxr-xr-x    3 ftp      ftp          4096 Sep 11 03:45 pub
| ftp-syst:
|   STAT:
| FTP server status:
|      Connected to ::ffff:10.6.32.20
|      Logged in as ftp
|      TYPE: ASCII
|      No session bandwidth limit
|      Session timeout in seconds is 300
|      Control connection is plain text
|      Data connections will be plain text
|      At session startup, client count was 3
|      vsFTPd 3.0.3 - secure, fast, stable
|_End of status
22/tcp  open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 0c:84:1b:36:b2:a2:e1:11:dd:6a:ef:42:7b:0d:bb:43 (RSA)
|   256 e2:5d:9e:e7:28:ea:d3:dd:d4:cc:20:86:a3:df:23:b8 (ECDSA)
|_  256 ec:be:23:7b:a9:4c:21:85:bc:a8:db:0e:7c:39:de:49 (ED25519)
139/tcp open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
445/tcp open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
Service Info: Host: NERDHERD; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Host script results:
|_clock-skew: mean: -39m59s, deviation: 1h09m16s, median: 0s
| nbstat: NetBIOS name: NERDHERD, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
| Names:
|   NERDHERD<00>         Flags: <unique><active>
|   NERDHERD<03>         Flags: <unique><active>
|   NERDHERD<20>         Flags: <unique><active>
|   \x01\x02__MSBROWSE__\x02<01>  Flags: <group><active>
|   WORKGROUP<00>        Flags: <group><active>
|   WORKGROUP<1d>        Flags: <unique><active>
|_  WORKGROUP<1e>        Flags: <group><active>
| smb-os-discovery:
|   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
|   Computer name: nerdherd
|   NetBIOS computer name: NERDHERD\x00
|   Domain name: \x00
|   FQDN: nerdherd
|_  System time: 2020-11-17T20:58:59+02:00
| smb-security-mode:
|   account_used: guest
|   authentication_level: user
|   challenge_response: supported
|_  message_signing: disabled (dangerous, but default)
| smb2-security-mode:
|   2.02:
|_    Message signing enabled but not required
| smb2-time:
|   date: 2020-11-17T18:58:58
|_  start_date: N/A
```

First we look into the ftp server. Via anonymous login we find 2 files `youfoundme.png` and `.jokesonyou/hellon3rd.txt`

Couln't find anything usefull using `strings` on the png image. Using exiftool we find an `owner name`
```
fijbxslz
```

The txt file contains 
```
all you need is in the leet
```

`hellon3rd.txt` is leet for `hellonerd.txt`

Hmmm, not sure what to do with this...
Let's move on for now.

We see that there is a samba share running. Using `smbmap -H $IP` we find
```
[+] Guest session       IP: 10.10.42.21:445     Name: 10.10.42.21
        Disk                                                    Permissions     Comment
        ----                                                    -----------     -------
        print$                                                  NO ACCESS       Printer Drivers
        nerdherd_classified                                     NO ACCESS       Samba on Ubuntu
        IPC$                                                    NO ACCESS       IPC Service (nerdherd server (Samba, Ubuntu))
```

We don't have permissions to see anything tho (guest access)

I used the `enum4linux` perl script which listed a lot of stuff but the only new information was that there is a user named `chuck`. Seems to be also a `nobody` user (Might be there by default tho) and also an `ftpuser` linux user.
```
S-1-5-21-2306820301-2176855359-2727674639-1000 NERDHERD\chuck (Local User)

```


Let's try to bruteforce the password for `chuck` with 
```
patator smb_login host=$IP user=chuck password=FILE0 0=rockyou.txt -x ignore:fgrep='STATUS_LOGON_FAILURE'
```

I thought about trying the `1337` port which translate to `leet`. When `nc $IP 1337` nothing happen but when we presss `return` we get a bad request which mean that this is an http server. (also found it by checking all ports with nmap)

So we stop the bruteforcing, not usefull anymore...

When browsing, we get an alert box saying to look further into the source.

We find a bunch of comments in the css section
```
<!--
	hmm, wonder what i hide here?
 -->

<!--
	maybe nothing? :)
 -->

```

There is this link 
```
<p>Maybe the answer is in <a href="https://www.youtube.com/watch?v=9Gc4QTqslN4">here</a>.</p>
```

At the end of the page which redirect to the `Surfin Bird` youtube video, probably a troll.

I downloaded an original apache page and diffed with the one we get... There really isn't much difference except for comments and the youtube video link.

Let's gobuster this.

We find `/admin` which is a login page.
In the source we find this comment :
```
<!--
	these might help:
		Y2liYXJ0b3dza2k= : aGVoZWdvdTwdasddHlvdQ==
-->
```

The first is definitely base64
```
cibartowski
```

But the "password" doesn't seems to be base64...

Ok soo, I had a look at the writeup because I wasn't sure what to do.

So turns out the image owner name that we found earlier is encoded using `vigenere`. The clue in the webpage to the `Surfin Bird` should have shown us that the `vigenere` key is `birdistheword`
hmmm... that was far from obvious...

Once we decrypt the `fijbxslz` we find `easypass` which is the password for `chuck` smb access.

We then use the smb client to connect to the `nerdherd_classified` share
```
smbclient //$IP/nerdherd_classified -U chuck
```

NOTE : Not sure why but when I use `smbclient -L //$IP/nerdherd_classified -U chuck`, I get 
```
Sharename       Type      Comment
        ---------       ----      -------
        print$          Disk      Printer Drivers
        nerdherd_classified Disk      Samba on Ubuntu
        IPC$            IPC       IPC Service (nerdherd server (Samba, Ubuntu))
SMB1 disabled -- no workgroup available
```

Which is kinda weird, why would smbclient try to use SMB1 when using `-L` ?

Anyhow, once we get access, we can retrieve the `secr3t.txt` file which contains:
```
Ssssh! don't tell this anyone because you deserved it this far:

        check out "/this1sn0tadirect0ry"

Sincerely,
        0xpr0N3rd
<3
```

Seems like the `/admin` was a big troll again.

we find `/this1sn0tadirect0ry/creds.txt`
```
alright, enough with the games.

here, take my ssh creds:
	
	chuck : th1s41ntmypa5s
```

So lets try to ssh into this box.

And we're in !

From the motd, we see that this server is running `Ubuntu 16.04` which is pretty old. Maybe we can exploit this.

We get `user.txt` flag
```
THM{7fc91d70e22e9b70f98aaf19f9a1c3ca710661be}
```

Couln't run `sudo`, didn't find any interesting binaries with capabilities

So now that we got access to the box, we can look at `/var/www/html` and confirm that there is nothing to do in `/admin` 

Looking at `searchsploit` for a `16.04` exploit, we found a bunch of them.
Ended up using `linux/local/45010.c` which gave us root access.

We find `/root/root.txt` but it contains this...
```
cmon, wouldnt it be too easy if i place the root flag here?
```

Kinda stupid in my opinion... but yeah, let's find the flag.

We can find all the `txt` files belonging to root using `find / -name "*.txt" -group root`

This give us a bunch of files, we can use the flag format to precisely find the flag
```
find / -name "*.txt" -group root -exec grep -l -o "THM{.*}" {} \;
```

And we find it in `/opt/.root` :
```
nOOt nOOt! you've found the real flag, congratz!

THM{5c5b7f0a81ac1c00732803adcee4a473cf1be693}
```

Seems like there is a bonus flag, let's try to find it using bruteforce approach
```
grep -R -l -o "THM{.*}" / 2>/dev/null
```

I guess eventually we would have found it but grepping through the entire file system is quite slow...

The hint says
```
brings back so many memories
```

Which made me think about looking at the `.bash_history` and here it was :
```
THM{a975c295ddeab5b1a5323df92f61c4cc9fc88207}
```

Yeah just to confirm, running `grep -R -l -o "THM{.*}" /root 2>/dev/null` found
```
/root/.bash_history
```

Running on the whole filesystem wasa bit overkill
