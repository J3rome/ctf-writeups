# Tryhackme.com Room : Classic Passwd

`https://tryhackme.com/room/classicpasswd`



This room is a bit different than the one I'm used to.

We got a binary file and we need to get a flag in it.



Just by running `strings` on the binary, we see 

```
THM{%d%d}
```

And a bunch of other strings.

Seems like the flag is dynamically generated at runtime so let's start `ghidra`



We got 2 interesting functions

```
vuln()
glf()
```



`vuln` does the authentication, if unsuccessfull it exit the program otherwise it continue and `glf` is called which print the flag.



We can easily retrieve the flag from the printf statement :

```c
printf("THM{%d%d}",0x638a78,0x2130);
```

Which gives

```
THM{65235128496}
```

I was curious as to what was the actual username.

Looking at the decompiled code we see :

```c
username_ground_truth = 0x6435736a36424741;
local_23e = 0x476b6439;
local_23a = 0x37;
printf("Insert your username: ");
__isoc99_scanf(&DAT_0010201b,username);
strcmp(username,(char *)&username_ground_truth);
```

`username_ground_truth` decodes to `d5sj6BGA`. I tried that as a username but it didn't work.



So i used another tool called `frida` to hookup in the function call. From there, I was able too hookup to `strcmp` and print the callee arguments :

```
AGB6js5d9dkG7
```

which is the correct username.

Immediatly looking at this we see that the begining is `username_ground_truth` reversed.

I guess this is because of `endianess` ?

But then even reversed, `username_ground_truth` = `AGB6js5d`.

Variables are declared as follow :

```
  undefined8 username_ground_truth;
  undefined4 local_23e;
  undefined2 local_23a;
  char username [512];
```

So I guess `local_23e` and `local_23a` are following `username_ground_truth`.

`strcmp` should read the chars, starting from `&username_ground_truth` until it find a `null` character.



If we combine the value of `local_23e` and `local_23a` reversed with the rest. We get

```
username_ground_truth = AGB6js5d
local_23e = 9dkG
local_23a = 7
```

Which gives us :

```
AGB6js5d9dkG7
```

So we got the correct username combining those variables, but why does `strcmp` stops there ? Where is the null byte ?

Ahhhh I think I got it.

running `file ./Challenge` we get :

```
Challenge: ELF 64-bit LSB shared object, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=b80ce38cb25d043128bc2c4e1e122c3d4fbba7f7, for GNU/Linux 3.2.0, not stripped
```

where `LSB` means `Least-significant byte first`. 

So we get a `null` byte because `username` contains a X chars and `512 - X` null bytes.

Since we are using `LSB` the null bytes comes first.

In theory, if we fill `username` with at least `512` values, strcmp should continue and include the content of `username` in the comparison.

I tried `echo $(python -c 'print("A"*600)') | frida-trace -i "strcmp" ./Challenge` but I guess `ASLR` is getting in the way.

The first time I executed this, it actually worked and I saw a bunch of `A` as the second parameter to `strcmp` but after that it wouldn't work (Somethime hanging, other time just not working)



Anyhow, I think that resolve the mystery.

