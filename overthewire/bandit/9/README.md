# Over The Wire -- Bandit 9

## Server
```
sshpass -p UsvVyFSfZZWbi6wgC7dAFyFuR6jQQUhR ssh -p 2220 -oStrictHostKeyChecking=no bandit9@bandit.labs.overthewire.org 
```

## Solution

Its a binary file that contains some strings in it. Preceded by `=` signs


`strings -n 15 data.txt ` :
```
========== the*2i"4
========== password
Z)========== is
&========== truKLdjsbJ5g7yyJ2X2R0o3a5HQJFuLk
```
