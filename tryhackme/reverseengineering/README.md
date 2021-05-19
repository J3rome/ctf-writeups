



## First crackme

When we decompile the binary in `ghidra` we get :

```c
undefined8 main(void)

{
  int iVar1;
  long in_FS_OFFSET;
  undefined4 local_1c;
  undefined2 local_18;
  char local_16 [6];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("enter password");
  local_1c = 0x30786168;
  local_18 = 0x72;
  __isoc99_scanf(&DAT_001008a3,local_16);
  iVar1 = strcmp(local_16,(char *)&local_1c);
  if (iVar1 == 0) {
    puts("password is correct");
  }
  else {
    puts("password is incorrect");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

So `strcmp` compare with `local_1c`. 

It will stop reading characters from `&local_1c` when it reach a `null` byte

Since the file is encoded in `LSB` (Least Significant Byte) the first byte after `local_18`  will be the last byte of `local_16` (our input). This is where we are gonna get a null byte which will stop the comparison.

Soo, the password is `local_1c + local_18` which is `0x7230786168`

We can use python do decode this 

```
python3 -c 'import binascii;binascii.a2b_hex("7230786168").decode()[::-1]'
```

Which gives us the password 

```
hax0r
```



## Second crackme

The second binary decompiles to :

```c
undefined8 main(void)

{
  long in_FS_OFFSET;
  int local_14;
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  puts("enter your password");
  __isoc99_scanf(&DAT_00100838,&local_14);
  if (local_14 == 0x137c) {
    puts("password is valid");
  }
  else {
    puts("password is incorrect");
  }
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return 0;
}
```

So here it's pretty easy.

`local_14` is an integer.

`0x137c` = `4988 ` which is the valid password.



## Third Crack me

The binary decompiles to

```c

undefined8 main(void)

{
  long in_FS_OFFSET;
  int success_counter;
  undefined2 magic_value;
  undefined filler_str;
  char input_str [24];
  long local_10;
  
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  magic_value = 0x7a61;
  filler_str = 0x74;
  puts("enter your password");
  __isoc99_scanf(&DAT_00100868,input_str);
  success_counter = 0;
  do {
    if (2 < success_counter) {
      puts("password is correct");
LAB_001007ae:
      if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
        __stack_chk_fail();
      }
      return 0;
    }
    if (input_str[success_counter] != *(char *)((long)&magic_value + (long)success_counter)) {
      puts("password is incorrect");
      goto LAB_001007ae;
    }
    success_counter = success_counter + 1;
  } while( true );
}
```

Took me a little longer to figure this one out.

What it does basically, is comparing each char of `input_str` with the chars in `magic_value` and `filler`. Only the first 3 characters are important.



We got the value string `0x747a61` which translate to `azt`

So the correct password is `azt` (or `aztGARBAGE`)



## Wrap up

* We could have got the password for the first crackme simply by using `strings`