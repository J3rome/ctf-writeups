from pwn import *

ip = '10.10.220.36'
port = 60179
test_payload = "yoloo\n"

def test_port(port, ip='10.10.220.36', payload="inferno\n"):
	conn = remote(ip, port)
	initial = conn.recvline(timeout=0.5)

	if len(initial) > 0:
		print(f"Got initial response on port {port}")
		return True

	conn.send(test_payload)
	time.sleep(0.2)
	resp = conn.recvline(timeout=0.5)

	if len(resp) > 0:
		print(f"Got response on port {port}")
		return True

	conn.close()


with open('all_ports','r') as f:
	all_ports = f.readlines()


valid_ports = []
for p in all_ports:
	if test_port(p):
		valid_ports.append(p)

print('done')
print("Valid ports : ")
print(valid_ports)
