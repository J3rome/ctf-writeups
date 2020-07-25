# Over The Wire -- Bandit 29

## Server
```
sshpass -p bbc96594b4e001778eee9975372716b2 ssh -p 2220 -oStrictHostKeyChecking=no bandit29@bandit.labs.overthewire.org 
```

## Solution

Cloned the repo `git clone ssh://bandit29-git@127.0.0.1/home/bandit29-git/repo`
Got a `readme.md` file :
```
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: <no passwords in production!>

```

We get the list of all branches using
```
git fetch --all
git branch -a
```

```
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/dev
  remotes/origin/master
  remotes/origin/sploits-dev
```

We checkout `dev` and find :

```
# Bandit Notes
Some notes for bandit30 of bandit.

## credentials

- username: bandit30
- password: 5b90576bedb2cc04c86a9e924ce42faf

```