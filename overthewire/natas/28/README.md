# Over The Wire -- Natas 28

## Server URL
```
http://natas28:JWwR438wkgTsNKBbcJoowyysdM82YjeF@natas28.natas.labs.overthewire.org
```

## Solution
We got a search input box that give us a list of jokes.

We don't have access to the source code

Seems to be vulnerable to sql injection

The paths are weird tho
```
/search.php/?query=G%2BglEae6W%2F1XjA7vRm21nNyEco%2Fc%2BJ2TdR0Qp8dcjPLWnBZ4e4lYiWEnLU8jGIqfmi4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo%3D
```

Look like the query is base64.
After urldecoding we get
```
G+glEae6W/1XjA7vRm21nNyEco/c+J2TdR0Qp8dcjPLWnBZ4e4lYiWEnLU8jGIqfmi4rXbbzHxmhT3Vnjq2qkEJJuT5N6gkJR5mVucRLNRo=
```

Decoding it as base64 give nothing.. Tried other bases as well, didn't work. Might be a combination of multiple bases one after the other ?


Seems to hang with this input `you' or 1=1 #`. Doesn't return anything (Might be a connection problem ?)

The page we are querying is `/search.php/index.php?query`
When visiting `/search.php` without a query we get the output
```
mep
```

Specifying a random query such as `/search.php/index.php?query=gogo` give us this error :
```
Incorrect amount of PKCS#7 padding for blocksize
```

Hmm interesting

We send character until the encoded query size change.
We find a block size of 16 characters

```
Nb Char : Len(encoded_query)
0  - 12 : 108
13 - 28 : 128
29 - 44 : 152
45 - 60 : 172
61 - 76 : 192
77 - 93 : 216
```