from pwn import remote

ip = "10.10.207.52"

port = 9000

conn = remote(ip, port)
print(conn.recvline())