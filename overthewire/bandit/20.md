# Over The Wire -- Bandit 20

## Server
```
sshpass -p GbKksEFF4yrVs6il55v6gwY5aVje5f0j ssh -p 2220 -oStrictHostKeyChecking=no bandit20@bandit.labs.overthewire.org 
```

## Solution

We have a binary with suid for user `bandit21`.

Running it give
```
Usage: ./suconnect <portnumber>
This program will connect to the given port on localhost using TCP. If it receives the correct password from the other side, the next password is transmitted back.
```

Oh well, not sure if i were supposed to scan for a service running on the machine that spit out the password ?

Anyhow, I just spawned a tcp connection using `nc -lnvp 8888` and used `./suconnect 8888`.
I then sent the current password via the first console and received :
```
gE269g2h3mw3pwgrj0Ha9Uoqen1c9DGr
```
