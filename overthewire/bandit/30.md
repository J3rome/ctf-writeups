# Over The Wire -- Bandit 30

## Server
```
sshpass -p 5b90576bedb2cc04c86a9e924ce42faf ssh -p 2220 -oStrictHostKeyChecking=no bandit30@bandit.labs.overthewire.org 
```

## Solution

Cloned the repo `git clone ssh://bandit30-git@127.0.0.1/home/bandit30-git/repo`
Got a `readme.md` file :
```
just an epmty file... muahaha
```

Looked around, finally found something in `git tag`.

Was able to retrieve the info using `git show secret`:
```
47e603bb428404d265f59c42920d81e5
```
