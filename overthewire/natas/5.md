# Over The Wire -- Natas 5

## Server URL
```
http://natas5:iX6IOfmpN7AYOQGPwtn3fXpbaJVJcHfq@natas5.natas.labs.overthewire.org
```

## Solution
The website says
```
You are not logged in
```

Looking at the cookies in the chrome inspector, we find the value `loggedIn` is set to 0.
We set it to 1 and refresh.

We get
```
Access granted. The password for natas6 is aGoY4q2Dc6MgDq4oL4YtoKtyAg9PeHa1
```
