# Over The Wire -- Bandit 18

## Server
```
sshpass -p kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd ssh -p 2220 -oStrictHostKeyChecking=no bandit18@bandit.labs.overthewire.org 
```

## Solution

Hmm, so the connection is closed right when we connect.

Let's try to execute some commands.

Yep we can execute `ls -la` and we find a `readme` file.

It contains the next password :
```
IueksS7Ubh8G3DCwVzrTd8rAVOwq3M5x
```