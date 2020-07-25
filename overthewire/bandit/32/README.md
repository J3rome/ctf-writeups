# Over The Wire -- Bandit 32

## Server
```
sshpass -p 56a9bf19c63d650ce78e6ec0354ee45e ssh -p 2220 -oStrictHostKeyChecking=no bandit32@bandit.labs.overthewire.org 
```

## Solution
We are in `UPPERCASE Shell`.
Everything is converted to uppercase...

I fiddled with this for a while. And then i thought of playing with the parameters variables.

`$0` contains `sh` which gave me a shell.

This shell have `bandit33` privileges because of setuid byte.

We can then read `cat /home/bandit33/README.txt`
```
Congratulations on solving the last level of this game!

At this moment, there are no more levels to play in this game. However, we are constantly working
on new levels and will most likely expand this game with more levels soon.
Keep an eye out for an announcement on our usual communication channels!
In the meantime, you could play some of our other wargames.

If you have an idea for an awesome new level, please let us know!
```

Sooo, that was fun !