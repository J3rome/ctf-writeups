# Over The Wire -- Bandit 6

## Server
```
sshpass -p DXjZPULLxYr17uwoI01bNLQbtFemEgo7 ssh -p 2220 -oStrictHostKeyChecking=no bandit6@bandit.labs.overthewire.org 
```

## Solution

We find the file that belong to user `bandit7` and group `bandit6` :
```
find / -user bandit7 -group bandit6 2>/dev/null
/var/lib/dpkg/info/bandit7.password
```

And we get the password :
```
HKBPTKQnIay4Fw76bEy8PVxKEDQRKTzs
```

