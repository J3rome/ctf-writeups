# Over The Wire -- Bandit 19

## Server
```
sshpass -p IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x ssh -p 2220 -oStrictHostKeyChecking=no bandit19@bandit.labs.overthewire.org 
```

## Solution

We have a suid binary that we can use to execute commands as `bandit20`.

We can read the password with `./bandit20-do cat /etc/bandit_pass/bandit20`
```
GbKksEFF4yrVs6il55v6gwY5aVje5f0j
```
