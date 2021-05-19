#!/usr/bin/env python3
import subprocess
import argparse
import psutil

parser = argparse.ArgumentParser()
parser.add_argument("--min_usage", type=int, default=100, help="Min swap usage in Mb")


def get_process_using_swap(min_usage_in_mb):
    # Only respect the number number of digits in min_usage_in_mb (100mb or 500mb will output the same thing)
    min_digit = len(str(min_usage_in_mb * 1000))

    ignore_pattern = " "
    for i in range(min_digit - 1):
        ignore_pattern += "\\d?"

    ignore_pattern += " kB"

    cmd = f'grep -H "VmSwap" /proc/*/status | grep -P -v "{ignore_pattern}" | sort -nk 2'

    return subprocess.check_output(cmd, shell=True).decode().strip().split("\n")[::-1]


def print_swap_usage(swap_lines, min_usage_in_mb):
    for swap_line in swap_lines:
        proc_info, usage = swap_line.split("\t ")

        usage = int(usage.replace(" kB",  "")) / 1000
        if usage < min_usage_in_mb or usage == 0:
            continue

        usage = f"{usage:.2f} Mb"

        pid = proc_info.replace("/proc/", "").split("/")[0]

        if not pid.isdigit():
            # Ignore non digit
            continue

        pid = int(pid)

        try:
            process = psutil.Process(pid)
        except psutil.NoSuchProcess:
            continue

        try:
            process_path = process.exe()
        except (PermissionError, psutil.AccessDenied):
            process_path = "ACCESS DENIED"

        print(f'   {usage: >10} --> {process.name(): <30} {process_path: <40} (Pid: {pid})')
        

if __name__ == "__main__":
    args = parser.parse_args()
    print(f"RAM used at {psutil.virtual_memory().percent}%")
    print(f"SWAP used at {psutil.swap_memory().percent}%\n")
    print(f"Showing process using at least {args.min_usage} Mb of Swap")

    swap_lines = get_process_using_swap(args.min_usage)
    print_swap_usage(swap_lines, args.min_usage)
