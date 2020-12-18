import subprocess
import itertools

values = ['1','2','3','4','5','6']

for comb in itertools.permutations(values):
	cmd = f"/usb/bin/blogFeedback {' '.join(comb)}"

	out = subprocess.check_output(cmd, shell=True)

	print(out)

	exit(0)

