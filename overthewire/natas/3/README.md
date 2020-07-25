# Over The Wire -- Natas 3

## Server URL
```
http://natas3:sJIJNW6ucpu6HPZ1ZAchaDtwd7oGrD14@natas3.natas.labs.overthewire.org
```

## Solution
We find a comment that says
```
Not even google will find it
```

We then check the `/robots.txt` file and find :
```
User-agent: *
Disallow: /s3cr3t/
```

We check `/s3cr3t`

We find `/s3cr3t/user.txt` :
```
natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ
```

