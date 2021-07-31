# Tryhackme.com Room : Battery

`https://tryhackme.com/room/battery`

## Instance

```bash
export IP="10.10.100.113"
```

## Nmap

```
22/tcp open  ssh     OpenSSH 6.6.1p1 Ubuntu 2ubuntu2 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey:
|   1024 14:6b:67:4c:1e:89:eb:cd:47:a2:40:6f:5f:5c:8c:c2 (DSA)
|   2048 66:42:f7:91:e4:7b:c6:7e:47:17:c6:27:a7:bc:6e:73 (RSA)
|   256 a8:6a:92:ca:12:af:85:42:e4:9c:2b:0e:b5:fb:a8:8b (ECDSA)
|_  256 62:e4:a3:f6:c6:19:ad:30:0a:30:a1:eb:4a:d3:12:d3 (ED25519)
80/tcp open  http    Apache httpd 2.4.7 ((Ubuntu))
| http-methods:
|_  Supported Methods: OPTIONS GET HEAD POST
|_http-server-header: Apache/2.4.7 (Ubuntu)
|_http-title: Site doesn't have a title (text/html).
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

## Initial Foothold

Not much on the landind page, let's gobuster



We find a folder `/scripts` with `jquery` js files. There is also a folder `/scripts/ie` with an empty `index.html` 



We find a binary file at `/report` 

By running `strings report` we find these strings

```
admin@bank.a
===============List of active users================
support@bank.a
contact@bank.a
cyber@bank.a
admins@bank.a
sam@bank.a
admin0@bank.a
super_user@bank.a
control_admin@bank.a
it_admin@bank.a
```



When executing the binary we are greeted by 

```
Welcome To ABC DEF Bank Managemet System!
```

And asked for a username & password.

We can login using `guest:guest`

```
===================Available Options==============
1. Check users
2. Add user
3. Delete user
4. change password
5. Exit
```



Looking at the binary in `Ghidra` doesn't seem like it does much. We can only login as guest, nothing happen with other username.

We can only "change password" when trying to change `admin@bank.a` but we can enter anything and we just get `password changed successfully` 

This seems like a dumb useless binary.



Sooo, gobuster didn't find anything usefull but `nikto` found an `admin.php` page with title `ABC DEF Bank Managemet login` 



We can't login with `guest:guest` on this one but we can create a new user.

We register with 2 fields

```
user
Bank Name
password
```

Maybe one of these is injectable ?

We see that `<?` is replaced to `<!--?` and `?>` to `?-->` which "prevent" php code execution.

Maybe we can find a way around this filter ?



In the form the username seems to have a maxlength of 12 (Maybe we can do a partial match with spaces)





## Priv esc



## End

