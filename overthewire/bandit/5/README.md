# Over The Wire -- Bandit 5

## Server
```
sshpass -p koReBOKuIDDepwhWk7jZC0RTdopnAYKh ssh -p 2220 -oStrictHostKeyChecking=no bandit5@bandit.labs.overthewire.org 
```

## Solution

We can get all the files with `find inhere -type f`.

The page says that the file as a size of 1033 bytes.

`find inhere -type f -size 1033c -exec cat {} \;` :
```
DXjZPULLxYr17uwoI01bNLQbtFemEgo7
```

