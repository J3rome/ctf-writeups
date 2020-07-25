# Over The Wire -- Bandit 14

## Server
```
sshpass -p 4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e ssh -p 2220 -oStrictHostKeyChecking=no bandit14@bandit.labs.overthewire.org 
```

## Solution

We retrieve the password `cat /etc/bandit_pass/bandit14`
```
4wcYUJFw0k0XLShlDzztnTBHiqxU3b3e
```

And send it to `nc 127.0.0.1 30000`

We get 
```
Correct!
BfMYroe26WYalil77FoDi9qh59eK5xNr
```