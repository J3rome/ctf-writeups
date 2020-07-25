# Over The Wire -- Natas 11

## Server URL
```
http://natas11:U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK@natas11.natas.labs.overthewire.org
```

## Solution
We can see the php source code :
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
<script>var wechallinfo = { "level": "natas11", "pass": "<censored>" };</script></head>
<?

$defaultdata = array( "showpassword"=>"no", "bgcolor"=>"#ffffff");

function xor_encrypt($in) {
    $key = '<censored>';
    $text = $in;
    $outText = '';

    // Iterate through each character
    for($i=0;$i<strlen($text);$i++) {
    $outText .= $text[$i] ^ $key[$i % strlen($key)];
    }

    return $outText;
}

function loadData($def) {
    global $_COOKIE;
    $mydata = $def;
    if(array_key_exists("data", $_COOKIE)) {
    $tempdata = json_decode(xor_encrypt(base64_decode($_COOKIE["data"])), true);
    if(is_array($tempdata) && array_key_exists("showpassword", $tempdata) && array_key_exists("bgcolor", $tempdata)) {
        if (preg_match('/^#(?:[a-f\d]{6})$/i', $tempdata['bgcolor'])) {
        $mydata['showpassword'] = $tempdata['showpassword'];
        $mydata['bgcolor'] = $tempdata['bgcolor'];
        }
    }
    }
    return $mydata;
}

function saveData($d) {
    setcookie("data", base64_encode(xor_encrypt(json_encode($d))));
}

$data = loadData($defaultdata);

if(array_key_exists("bgcolor",$_REQUEST)) {
    if (preg_match('/^#(?:[a-f\d]{6})$/i', $_REQUEST['bgcolor'])) {
        $data['bgcolor'] = $_REQUEST['bgcolor'];
    }
}

saveData($data);



?>

<h1>natas11</h1>
<div id="content">
<body style="background: <?=$data['bgcolor']?>;">
Cookies are protected with XOR encryption<br/><br/>

<?
if($data["showpassword"] == "yes") {
    print "The password for natas12 is <censored><br>";
}

?>

<form>
Background color: <input name=bgcolor value="<?=$data['bgcolor']?>">
<input type=submit value="Set color">
</form>

<div id="viewsource"><a href="index-source.html">View sourcecode</a></div>
</div>
</body>
</html>
```

We got a cookie we encoded data.
The data as the following json form
```json
{
	"showpassword": "no",
	"bgcolor": "#ffffff"
}
```

We want to put the value `yes` in `showpassword`.

The cookie is encoded as follow :
```
Json Stringify - json_encode()
xor encrypt - With secret key
Base 64 encode
```

Since we know what the encoded message is, we can reverse the xor by xoring with the message.

We write a python script to retrieve the key from the original cookie value, create a new cookie and send the request to the page with this cookie :
```py
import base64
import json
import requests

def do_xor(to_encode, key):
	out = []
	for i, word in enumerate(to_encode):
		out.append(ord(word) ^ ord(key[i % len(key)]))

	return "".join([chr(o) for o in out])

def retrieve_key_from_potential(potential_key):
	# This will extract the key when presented a string with the format "keykeykeykeykey"
	# Will take the first repeating pattern. Pattern must start at the beginning of the string
	current = ""

	for i, letter in enumerate(potential_key):
		current += letter

		next_word = potential_key[i+1:i + 1 + len(current)]

		if current == next_word :
			return current

	return None

url = "http://natas11:U82q5TCMMQ9xuFoI3dYX61s7OZD9JKoK@natas11.natas.labs.overthewire.org"

cookie = "ClVLIh4ASCsCBE8lAxMacFMZV2hdVVotEhhUJQNVAmhSEV4sFxFeaAw="
# php json encode result in a string without any space while python json.dumps add spaces. We must specify separators
content = json.dumps({'showpassword':'no', 'bgcolor':"#ffffff"}, separators=(',', ":"))

to_decode = base64.b64decode(bytes(cookie, 'utf-8')).decode('utf-8')

potential_key = do_xor(to_decode, content)

key = retrieve_key_from_potential(potential_key)

new_cookie = do_xor(json.dumps({'showpassword': 'yes', 'bgcolor': '#ffffff'}), key)
new_cookie = base64.b64encode(bytes(new_cookie, 'utf-8')).decode('utf8')

r = requests.get(url, cookies={'data': new_cookie})

next_password = r.text.split('The password for natas12 is ')[1].split('<br>')[0]

print(f"Natas12 password is {next_password}")
```

We get the password :
```
EDXp0pS26wLKHZy1rDBPUZk0RKfLGIR3
```

