# Over The Wire -- Bandit 4

## Server
```
sshpass -p pIwrPrtPN36QITSp3EQaw936yaFoFgAB ssh -p 2220 -oStrictHostKeyChecking=no bandit4@bandit.labs.overthewire.org 
```

## Solution

Files starts with the `-` character (`-file01`)

when in `inhere` folder, `cat *` won't work because of the `-`.

We can read all files with `cat inhere/*` or `cat ./*`

We could also disable argument parsing using `--` -> `cat -- *`

We get the password
```
MkoReBOKuIDDepwhWk7jZC0RTdopnAYKh
```

But this is wrong...

Using `strings` we get a better result

`strings -- *` : 
```
!TQO
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```

Here is the password for bandit5
```
koReBOKuIDDepwhWk7jZC0RTdopnAYKh
```