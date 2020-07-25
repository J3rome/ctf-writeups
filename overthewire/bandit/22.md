# Over The Wire -- Bandit 22

## Server
```
sshpass -p Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI ssh -p 2220 -oStrictHostKeyChecking=no bandit22@bandit.labs.overthewire.org 
```

## Solution
We look at cronjobs in `/etc/cron.d` as suggested.

We find `cronjob_bandit23`. it call the script `/usr/bin/cronjob_bandit23.sh`
```bash
#!/bin/bash

myname=$(whoami)
mytarget=$(echo I am user $myname | md5sum | cut -d ' ' -f 1)

echo "Copying passwordfile /etc/bandit_pass/$myname to /tmp/$mytarget"

cat /etc/bandit_pass/$myname > /tmp/$mytarget
```

The script will be runned as `bandit23` so we can get the `mytarget` using `echo I am user bandit23 | md5sum | cut -d ' ' -f 1`. We get :
```
8ca319486bfbbc3663ea0fbe81326349
```

We `cat /tmp/8ca319486bfbbc3663ea0fbe81326349`
```
jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n
```
