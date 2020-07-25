import sys
import requests
import time

def get_initial_port(ip):
	# Quick and dirty parsing
	r = requests.get(f'http://{ip}:3010')
	t = r.text.split('id="onPort">')[1]
	t = t.split("</a>")[0]
	return int(t)

ip = "10.10.56.89"
print("Waiting for port 1337...")

port = get_initial_port(ip)
while port != 1337:
	port = get_initial_port(ip)
	time.sleep(3)

print(f"Starting...")

current = 0
while True:
	try:
		r = requests.get(f"http://{ip}:{port}")
	except:
		# We just hammer the server while waiting to the port to open
		continue

	splitted = r.text.split(' ')

	if len(splitted) != 3 or port == 9765:
		print(r.text)
		print(f"Current number : {current}")
		exit(0)

	last_port = port
	operation, val, port = splitted

	print(f"Current Value: {current}")
	print(f"Operation : {operation} -- Operande : {val}")
	print(f"Port : {last_port} -> {port}")

	val = float(val)

	if operation == "add":
		current += val
	elif operation == "minus":
		current -= val
	elif operation == "multiply":
		current *= val
	elif operation == "divide":
		current /= val
	else:
		print(f"Unknown operation : {operation}")
		exit(0)

	time.sleep(2)
