import subprocess
import argparse

parser = argparse.ArgumentParser('Experiment Runner')
parser.add_argument("--ip", type=str, default="10.10.156.230", help="Server ip")
parser.add_argument("--start_port", type=int, default=2500, help="Start port")
parser.add_argument("--end_port", type=int, default=4000, help="End port")

args = parser.parse_args()

for port in range(args.start_port, args.end_port):
    print("="*40, flush=True)
    print(f"Port : {port}", flush=True)
    try:
        out = subprocess.check_output(f"ssh -p {port} hades@{args.ip}", shell=True, timeout=1.5, stderr=subprocess.STDOUT)
    except subprocess.TimeoutExpired as e:
        print("------TIMEOUT EXPIRED------", flush=True)
        continue
    except subprocess.CalledProcessError as e:
        print("non-zero exit", flush=True)
        out = e.output
        #continue

    try:
        out = out.decode().strip()
    except:
        print("Couldn't decode... printing bytes", flush=True)
    print(out, flush=True)

print("Done...", flush=True)