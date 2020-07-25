# Over The Wire -- Bandit 13

## Server
```
sshpass -p 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL ssh -p 2220 -oStrictHostKeyChecking=no bandit13@bandit.labs.overthewire.org 
```

## Solution

We retrieve the private key using `scp` and login as `bandit14`

```
ssh -p -i bandit14.key bandit14@bandit.labs.overthewire.org
```