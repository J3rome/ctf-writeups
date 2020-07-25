# Over The Wire -- Bandit 21

## Server
```
sshpass -p gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr ssh -p 2220 -oStrictHostKeyChecking=no bandit21@bandit.labs.overthewire.org 
```

## Solution
We look at cronjobs in `/etc/cron.d` as suggested.

We find `cronjob_bandit22`. it call the script `/usr/bin/cronjob_bandit22.sh`
```bash
#!/bin/bash
chmod 644 /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
cat /etc/bandit_pass/bandit22 > /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv
```

We `cat /tmp/t7O6lds9S0RqQh9aMcz6ShpAoZKF7fgv`
```
Yk7owGAcWjwMVRwrTesJEwB7WVOiILLI
```
