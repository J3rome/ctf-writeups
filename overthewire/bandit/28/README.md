# Over The Wire -- Bandit 28

## Server
```
sshpass -p 0ef186ac70e04ea33b4c1853d2526fa2 ssh -p 2220 -oStrictHostKeyChecking=no bandit28@bandit.labs.overthewire.org 
```

## Solution

Cloned the repo `git clone ssh://bandit28-git@127.0.0.1/home/bandit28-git/repo`
Got a `readme.md` file :
```
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: xxxxxxxxxx
```

By going one commit before, we can retrieve the content `git checkout c086d11a00c0648d095d04c089786efef5e01264`
```
# Bandit Notes
Some notes for level29 of bandit.

## credentials

- username: bandit29
- password: bbc96594b4e001778eee9975372716b2
```