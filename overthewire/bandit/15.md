# Over The Wire -- Bandit 15

## Server
```
sshpass -p BfMYroe26WYalil77FoDi9qh59eK5xNr ssh -p 2220 -oStrictHostKeyChecking=no bandit15@bandit.labs.overthewire.org 
```

## Solution

We open an SSL connection with `openssl s_client -connect 127.0.0.1:30001`

We send bandit15 password and receive:
```
Correct!
cluFn7wTiGryunymYOu4RcffSxQluehd
```
