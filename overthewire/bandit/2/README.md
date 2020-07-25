# Over The Wire -- Bandit 2

## Server
```
sshpass -p CV1DtqXWVFXTvM2F0k09SHz0YwRINYA9 ssh -p 2220 -oStrictHostKeyChecking=no bandit2@bandit.labs.overthewire.org 
```

## Solution

There is a file with spaces in the filename.

We can easily use the autocomplete for this (Or quotes or manual escape...)

```
cat spaces\ in\ this\ filename 
UmHadQclWmgdLOKQ3YNgjWxGoRMb5luK
```
