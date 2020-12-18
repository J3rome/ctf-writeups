import subprocess

start=1000000
end=9999999

for i in range(start, end):
	out = subprocess.check_output(f'echo {i} | ./try-harder', shell=True).decode()

	print(i)

	if 'Incorrect' not in out:
		print("GOTCHA !!")
		print(f"---{i}----")
		break
