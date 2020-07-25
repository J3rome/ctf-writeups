# Over The Wire -- Bandit 12

## Server
```
sshpass -p 5Te8Y4drgCRfCx8ugdwuEX8KFC6k2EUu ssh -p 2220 -oStrictHostKeyChecking=no bandit12@bandit.labs.overthewire.org 
```

## Solution

We got a datadump of a file.

We can recreate the file using `xxd -r data.txt > /tmp/hex`

We see that its a gzip with `file /tmp/hex`
```
/tmp/hex: gzip compressed data, was "data2.bin", last modified: Thu May  7 18:14:30 2020, max compression, from Unix
```

We got to rename to file with the `.gz` extension for the cmd to work (probably a way to force without the extension)

Then we get multiple archives, `bzip2`, `tar` and more `gzip`.
We finally get
```
The password is 8ZjyCRiBWFYkneahHwxCv3wb2a1ORpYL
```
