# Over The Wire -- Natas 27

## Server URL
```
http://natas27:55TBjpPZUUJgVP5b3BnbG6ON9uDPVzCJ@natas27.natas.labs.overthewire.org
```

## Solution
We get a login prompt (Username & Password)

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
<script>var wechallinfo = { "level": "natas27", "pass": "<censored>" };</script></head>
<body>
<h1>natas27</h1>
<div id="content">
<?

// morla / 10111
// database gets cleared every 5 min 


/*
CREATE TABLE `users` (
  `username` varchar(64) DEFAULT NULL,
  `password` varchar(64) DEFAULT NULL
);
*/


function checkCredentials($link,$usr,$pass){
 
    $user=mysql_real_escape_string($usr);
    $password=mysql_real_escape_string($pass);
    
    $query = "SELECT username from users where username='$user' and password='$password' ";
    $res = mysql_query($query, $link);
    if(mysql_num_rows($res) > 0){
        return True;
    }
    return False;
}


function validUser($link,$usr){
    
    $user=mysql_real_escape_string($usr);
    
    $query = "SELECT * from users where username='$user'";
    $res = mysql_query($query, $link);
    if($res) {
        if(mysql_num_rows($res) > 0) {
            return True;
        }
    }
    return False;
}


function dumpData($link,$usr){
    
    $user=mysql_real_escape_string($usr);
    
    $query = "SELECT * from users where username='$user'";
    $res = mysql_query($query, $link);
    if($res) {
        if(mysql_num_rows($res) > 0) {
            while ($row = mysql_fetch_assoc($res)) {
                // thanks to Gobo for reporting this bug!  
                //return print_r($row);
                return print_r($row,true);
            }
        }
    }
    return False;
}


function createUser($link, $usr, $pass){

    $user=mysql_real_escape_string($usr);
    $password=mysql_real_escape_string($pass);
    
    $query = "INSERT INTO users (username,password) values ('$user','$password')";
    $res = mysql_query($query, $link);
    if(mysql_affected_rows() > 0){
        return True;
    }
    return False;
}


if(array_key_exists("username", $_REQUEST) and array_key_exists("password", $_REQUEST)) {
    $link = mysql_connect('localhost', 'natas27', '<censored>');
    mysql_select_db('natas27', $link);
   

    if(validUser($link,$_REQUEST["username"])) {
        //user exists, check creds
        if(checkCredentials($link,$_REQUEST["username"],$_REQUEST["password"])){
            echo "Welcome " . htmlentities($_REQUEST["username"]) . "!<br>";
            echo "Here is your data:<br>";
            $data=dumpData($link,$_REQUEST["username"]);
            print htmlentities($data);
        }
        else{
            echo "Wrong password for user: " . htmlentities($_REQUEST["username"]) . "<br>";
        }        
    } 
    else {
        //user doesn't exist
        if(createUser($link,$_REQUEST["username"],$_REQUEST["password"])){ 
            echo "User " . htmlentities($_REQUEST["username"]) . " was created!";
        }
    }

    mysql_close($link);
} else {
?>

<form action="index.php" method="POST">
Username: <input name="username"><br>
Password: <input name="password" type="password"><br>
<input type="submit" value="login" />
</form>
<? } ?>
<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

Entering a username and password will create a user using this query :
```php
$query = "SELECT username from users where username='$user' and password='$password' ";
```

Login in with those credentials will give us a dump of our data
```
Array ( [username] => yolo [password] => fatkid )
```

Seems like user `natas28` exist, but user `natas27` also exist... Maybe someone else created them ? The database get cleared every 5 minutes tho so thats probaby the user we need to retrieve.

All strings seems to go through `mysql_real_escape_string`

The `username` is displayed on page but enclosed inside `htmlentities`
Same for the dumped data.

Hmmm.. kinda stuck here, can't think of a way to solve this.

Let's check writeups.

First thing that is pointed out is the loop when dumping the data.
It means that selecting for a user might return more than one row but we return just the first one.
We probably need to create a duplicate `natas28` user, but how ?

Couldn't figure it out, looked up the write up again and they mention that when `select`, trailing spaces are not used/trimmed. So `SELECT * from users where username='natas28'` is the same as `SELECT * from users where username='natas28 '`.

But with this technique, we can't bypass the `validUser` function.

Skimmed a bit more in the write up, they talk about the max size of the field and this is where it all clicked (well.. i pretty much had everything at this point...).

When inserting a string longer than the field length, the exceeding characters are truncated.

Knowing that `select 'value'` will also capture `'value  '`, we can create a new user with spaces up until the field length and a letter at the end.

Our input is:
```
natas28                                                         n
```

This way, the newly inserted name will be truncated to (Lots of spaces at the end)
```
natas28                                                         
```

When login in with `natas28`, the `checkCredentials` function will find the entry with natas28 followed by spaces with OUR password.

It will then log us in as `natas28`

Since the `dumpData` function will only return the first row, we get the password for the real natas28:
```
JWwR438wkgTsNKBbcJoowyysdM82YjeF
```
