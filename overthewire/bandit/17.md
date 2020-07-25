# Over The Wire -- Bandit 17

## Server
```
sshpass -p xLYVMN9WE5zQ5vHacb0sZEVqbrp7nBTn ssh -p 2220 -oStrictHostKeyChecking=no bandit17@bandit.labs.overthewire.org 
```

## Solution

We can simply diff the file `diff passwords.old passwords.new`
```
42c42
< w0Yfolrc5bwjS4qw5mq1nnQi6mF03bii
---
> kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
```

The password for bandit18 is 
```
kfBf3eYk5BPBRzwjqutbbfE887SVc5Yd
```