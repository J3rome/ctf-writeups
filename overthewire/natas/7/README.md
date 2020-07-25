# Over The Wire -- Natas 7

## Server URL
```
http://natas7:7z3hEENjQtflzgnT29q7wAvMNfZdh0i9@natas7.natas.labs.overthewire.org
```

## Solution
We can browse page with the `page` query parameters.
There is probably a `local file inclusion`. 
There is a hint in the html comments :
```
<!-- hint: password for webuser natas8 is in /etc/natas_webpass/natas8 -->
```

Let's try to browse this file using `/index.php?page=/etc/natas_webpass/natas8`
And we get the password :
```
DBfUBfqQG69KvJvJ1iAbMoIpwSNQ9bWe
```