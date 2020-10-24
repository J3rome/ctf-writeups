# Tryhackme.com Room : Gotta catch them all
`https://tryhackme.com/room/pokemon`


# Instance
```
export IP=10.10.89.38
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.8 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 58:14:75:69:1e:a9:59:5f:b2:3a:69:1c:6c:78:5c:27 (RSA)
|   256 23:f5:fb:e7:57:c2:a5:3e:c2:26:29:0e:74:db:37:c2 (ECDSA)
|_  256 f1:9b:b5:8a:b9:29:aa:b6:aa:a2:52:4a:6e:65:95:c5 (EdDSA)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Can You Find Them All?
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

Lets run gobuster on webserver... Nothing..

Looking at the source, we find the following HTML :
```
<pokemon>:<hack_the_pokemon>
        	<!--(Check console for extra surprise!)-->
      </hack_the_pokemon></pokemon>
```

We find the SSH credentials
```
pokemon:hack_the_pokemon
```

We find a zip file in `~/Desktop`
We unzip and find the grass-type pokemon. It is encoded as HEX.
Once decoded we get
```
PoKeMoN{Bulbasaur}
```

We look into `/var/www/html` and find `water-type.txt`
```
Ecgudfxq_EcGmP{Ecgudfxq}
```

Look like ROT encoding.
We use an online tool to test all ROT value and find that the shift value is 12. we get
```
Squirtle_SqUaD{Squirtle}
```

For the last pokemon, we can use `find . -name fire-type.txt` and we find the location of the file
```
/etc/why_am_i_here?/fire-type.txt
```

It is base64 encoded :
```
UDBrM20wbntDaGFybWFuZGVyfQ==
```

We get 
```
P0k3m0n{Charmander}
```

We saw `roots-type.txt` in `/home` but we need root access to get it.

We find a file in `/home/pokemon/Videos/Gotta/Catch/Them/ALL!/Could_this_be_what_Im_looking_for?.cplusplus`

We find the creds for user `ash`:
```
ash:pikapika
```

We got sudo right so we `sudo su`

And we find the `/home/roots-pokemon.txt`
```
Pikachu!
```

Anddd it's done