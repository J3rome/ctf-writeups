# Tryhackme.com Room : Source

`https://tryhackme.com/room/source`

## Instance

```bash
export IP="10.10.134.236"
```

## Nmap

```
PORT      STATE SERVICE VERSION
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 b7:4c:d0:bd:e2:7b:1b:15:72:27:64:56:29:15:ea:23 (RSA)
|   256 b7:85:23:11:4f:44:fa:22:00:8e:40:77:5e:cf:28:7c (ECDSA)
|_  256 a9:fe:4b:82:bf:89:34:59:36:5b:ec:da:c2:d3:95:ce (ED25519)
10000/tcp open  http    MiniServ 1.890 (Webmin httpd)
|_http-favicon: Unknown favicon MD5: 98860C3C5B095165D61D626EFFEDCC1B
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: Site doesn't have a title (text/html; Charset=iso-8859-1).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

We got `webmin` running.

Apparently there is a backdoor that have been planted in version `890` (Supply chain attack)

Tried to run manually this exploit `https://www.exploit-db.com/exploits/47293` but for some reason it didn't work.



Then launched `metasploit` used `linux/http/webmin_backdoor` and just like that, we get a `root` shell



`/home/dark/user.txt`:

```
THM{SUPPLY_CHAIN_COMPROMISE}
```



`/root/root.txt`:

```
THM{UPDATE_YOUR_INSTALL}
```

