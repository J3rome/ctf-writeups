# Over The Wire -- Bandit 8

## Server
```
sshpass -p cvX2JJa4CFALtqS87jk27qwqGhBM9plV ssh -p 2220 -oStrictHostKeyChecking=no bandit8@bandit.labs.overthewire.org 
```

## Solution

The password is the only line that is not repeated

`sort -n data.txt | uniq -c | grep "1 "` :
```
      1 UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR
```
