# Over The Wire -- Bandit 10

## Server
```
sshpass -p truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk ssh -p 2220 -oStrictHostKeyChecking=no bandit10@bandit.labs.overthewire.org 
```

## Solution

Password is encoded in base64.
`cat data.txt | base64 -d`
```
The password is IFukwKGsFW8MOq3IRFqrxE1hxTNEbUPR
```
