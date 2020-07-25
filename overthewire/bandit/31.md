# Over The Wire -- Bandit 31

## Server
```
sshpass -p 47e603bb428404d265f59c42920d81e5 ssh -p 2220 -oStrictHostKeyChecking=no bandit31@bandit.labs.overthewire.org 
```

## Solution

Cloned the repo `git clone ssh://bandit31-git@127.0.0.1/home/bandit31-git/repo`
Got a `readme.md` file :
```
This time your task is to push a file to the remote repository.

Details:
    File name: key.txt
    Content: 'May I come in?'
    Branch: master
```

I create the file, commit and push and receive this message :
```
remote: ### Attempting to validate files... ####
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
remote: 
remote: Well done! Here is the password for the next level:
remote: 56a9bf19c63d650ce78e6ec0354ee45e
remote: 
remote: .oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.oOo.
```

The password is :
```
56a9bf19c63d650ce78e6ec0354ee45e
```
