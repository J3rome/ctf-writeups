# Tryhackme.com Room : Looking Glass
`https://tryhackme.com/room/lookingglass`


# Instance
```
export IP=10.10.38.71
```

# Nmap
```
22/tcp    open  ssh        OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 3f:15:19:70:35:fd:dd:0d:07:a0:50:a3:7d:fa:10:a0 (RSA)
|   256 a8:67:5c:52:77:02:41:d7:90:e7:ed:32:d2:01:d9:65 (ECDSA)
|_  256 26:92:59:2d:5e:25:90:89:09:f5:e5:e0:33:81:77:6a (ED25519)
9000/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9001/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9002/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9003/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9009/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9010/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9011/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9040/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9050/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9071/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9080/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9081/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9090/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9091/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9099/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9100/tcp  open  jetdirect?
9101/tcp  open  jetdirect?
9102/tcp  open  jetdirect?
9103/tcp  open  jetdirect?
9110/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9111/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9200/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9207/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9220/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9290/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9415/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9418/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9485/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9500/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9502/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9503/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9535/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9575/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9593/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9594/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9595/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9618/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9666/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9876/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9877/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9878/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9898/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9900/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9917/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9929/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9943/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9944/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9968/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9998/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
9999/tcp  open  ssh        Dropbear sshd (protocol 2.0)
| ssh-hostkey: 
|_  2048 ff:f4:db:79:a9:bc:b8:8a:d4:3f:56:c2:cf:cb:7d:11 (RSA)
MAC Address: 02:F0:10:31:12:ED (Unknown)
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel
```

lots of ports open, lets poke around.


More ports open when running full port range scan :
```
10000/tcp open  snet-sensor-mgmt
to
13999/tcp open  unknown
```

All the ports from the "normal range" scan are
```
Dropbear sshd
```

Actually, they are all dropbear sshd... hmmmm

The hint says :
```
O(log n) A looking glass is a mirror.
```

When connecting with netcat on any ports we receive
```
SSH-2.0-dropbear
```

If we send back the same string, we get 
```
�2N�ğ8?}����:qcurve25519-sha256@libssh.org,ecdh-sha2-nistp256,ecdh-sha2-nistp384,ecdh-sha2-nistp521,diffie-hellman-group14-sha1ssh-rsaUaes128-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctrUaes128-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctrBhmac-sha2-256-etm@openssh.com,hmac-sha2-256,hmac-sha1,hmac-sha1-96Bhmac-sha2-256-etm@openssh.com,hmac-sha2-256,hmac-sha1,hmac-sha1-96nonenone��Sb�*�V��؞wZ
```

Not sure what we can do with this, the hint does mention `O(log n)` so we might need to send `SSH-2.0-dropbear` to every ports and see if we get a different response at some point.
Otherwise, we will have to dig a bit more into what is this... Seems to mention a bunch of encryption methods. 

Is this the first packet of the ssh handshake with dropbear ?

Ok soo, I was going in the wrong direction with this. Since it is ssh, I should just connect with ssh.

When we connect to a port, we get either `Lower` or `higher` which are cues to find the correct port

At first I was writing a script to script to do the search but I endend up doing a "binary search" by hand. Was pretty lucky, took about 5 min to find the correct port

```
ssh $IP -p 10765 -o "StrictHostKeyChecking=no"  
```

```
You've found the real service.
Solve the challenge to get access to the box
Jabberwocky
'Mdes mgplmmz, cvs alv lsmtsn aowil
Fqs ncix hrd rxtbmi bp bwl arul;
Elw bpmtc pgzt alv uvvordcet,
Egf bwl qffl vaewz ovxztiql.

'Fvphve ewl Jbfugzlvgb, ff woy!
Ioe kepu bwhx sbai, tst jlbal vppa grmjl!
Bplhrf xag Rjinlu imro, pud tlnp
Bwl jintmofh Iaohxtachxta!'

Oi tzdr hjw oqzehp jpvvd tc oaoh:
Eqvv amdx ale xpuxpqx hwt oi jhbkhe--
Hv rfwmgl wl fp moi Tfbaun xkgm,
Puh jmvsd lloimi bp bwvyxaa.

Eno pz io yyhqho xyhbkhe wl sushf,
Bwl Nruiirhdjk, xmmj mnlw fy mpaxt,
Jani pjqumpzgn xhcdbgi xag bjskvr dsoo,
Pud cykdttk ej ba gaxt!

Vnf, xpq! Wcl, xnh! Hrd ewyovka cvs alihbkh
Ewl vpvict qseux dine huidoxt-achgb!
Al peqi pt eitf, ick azmo mtd wlae
Lx ymca krebqpsxug cevm.

'Ick lrla xhzj zlbmg vpt Qesulvwzrr?
Cpqx vw bf eifz, qy mthmjwa dwn!
V jitinofh kaz! Gtntdvl! Ttspaj!'
Wl ciskvttk me apw jzn.

'Awbw utqasmx, tuh tst zljxaa bdcij
Wph gjgl aoh zkuqsi zg ale hpie;
Bpe oqbzc nxyi tst iosszqdtz,
Eew ale xdte semja dbxxkhfe.
Jdbr tivtmi pw sxderpIoeKeudmgdstd
Enter Secret:
```

Using `https://www.boxentriq.com/code-breaking/vigenere-cipher` we find the vigenere key: 
```
habetcipherthealp
```

The decoded message is :
```
Caaxlpozvgh
'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe.

'Beware the Jabberwock, my son!
The jaws that bite, the claws that catch!
Beware the Jubjub bird, and shun
The frumious Bandersnatch!'

He took his vorpal sword in hand:
Long time the manxome foe he sought--
So rested he by the Tumtum tree,
And stood awhile in thought.

And as in uffish thought he stood,
The Jabberwock, with eyes of flame,
Came whiffling through the tulgey wood,
And burbled as it came!

One, two! One, two! And through and through
The vorpal blade went snicker-snack!
He left it dead, and with its head
He went galumphing back.

'And hast thou slain the Jabberwock?
Come to my arms, my beamish boy!
O frabjous day! Callooh! Callay!'
He chortled in his joy.

'Twas brillig, and the slithy toves
Did gyre and gimble in the wabe;
All mimsy were the borogoves,
And the mome raths outgrabe.
Your secret is bewareTheJabberwock
```

After entering the code we get
```
jabberwock:RelievedDoubtfullyRestedStarting
```

We can use that as ssh credentials
.... And we are in
```
uid=1001(jabberwock) gid=1001(jabberwock) groups=1001(jabberwock)
```

User flag is reversed :
```
cat user.txt | rev
thm{65d3710e9d75d5f346d2bac669119a23}
```

Looking at `sudo -l` we got
```
(root) NOPASSWD: /sbin/reboot
```

Oh well, looking at the actual file :
```
lrwxrwxrwx 1 root root 14 May  3 11:30 /sbin/reboot -> /bin/systemctl*
```

At this point, we can probably override the symlink, but we can also escalte via systemctl i guess ?

So we can't override the symlink, and the first method on gtfo bins to explit systemctl didn't work. We dont have the rights to modify the variable `SYSTEMD_EDITOR`

I just put this aside for a bit and poked around the file system

We can browse `/home/alice`

We find an ssh key 
```
ll /home/alice/.ssh/id_rsa
-rw------- 1 humptydumpty humptydumpty 1679 Jul  3 01:26 .ssh/id_rsa
```

Belong to user `humptydumpty` ?

We also have an authorized key:
```
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDGY+dwBeKw2NtTbGLN+3hpg+qZ9ebXvfkU+UZ/iP0TFmGWaYM0hFyE9oVSoldBmLmvJAfpjFk/kgglcQ0r5rhahEPI+jIYr/retdOf8hZYpCRr21DbGt2fLF3Bu2Io/Uvhur/i9Tc5RwD5pgfGqHKrf1qul5x4dWK36NU+uIeIIDveTuAcKCmTBZzM1rkwwaj7UKDiJ/N9+/i6E+TEEsuXd/isF/zhGa4oQTLpthn79Y4SAeV+SzmeAWeJbvHZHe/KrvHIOvCJcSN9bjJh76QuIZnLKTWJrscaE0qkhG5890l1P6s0auNgUuOHN5ZgGYfHsmSGQRQUhXHplXXL6CKF alice@looking-glass
```

I was playing around with the `reboot` command and got bitten.. the machine restarted, the port changed, and the password also changed.

The secret to the hidden service is the same tho.
The new credentials are :
```
jabberwock:NicelySayingPointedStroke
```

There is a script in the `home/jabberwock`

This script is runned by `tweedledum`. Let's get a reverse shell. Took quite a while to get this executed tho. Actually, it was there after a reboot. Maybe its the reboot that trigger this ?

Let's reboot again.. Hopefully, not for nothing

We got a reverse shell to `tweedledum` upon reboot !

we find a the file `/home/tweedledum/humptydumpty.txt`
```
dcfff5eb40423f055a4cd0a8d7ed39ff6cb9816868f5766b4088b9e9906961b9
7692c3ad3540bb803c020b3aee66cd8887123234ea0c6e7143c0add73ff431ed
28391d3bc64ec15cbb090426b04aa6b7649c3cc85f11230bb0105e02d15e3624
b808e156d18d1cecdcc1456375f8cae994c36549a07c8c2315b473dd9d7f404f
fa51fd49abf67705d6a35d18218c115ff5633aec1f9ebfdc9d5d4956416f57f6
b9776d7ddf459c9ad5b0e1d6ac61e27befb5e99fd62446677600d7cacef544d0
5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8
7468652070617373776f7264206973207a797877767574737271706f6e6d6c6b
```

We decode this has hex and get a bunch of gibberish but at the end of the string we have
```
the password is zyxwvutsrqponmlk
```

Which is probably the password for humpydumpty

Hmmm.. doesn't work..

This is actually `klmnopqrstuvwxyz` reversed...

Ok sooo, my shell died, had to doo the whole dance again.

Added quick and dirty persistence by adding a cronjob that launch a reverse shell

I now have
```
Reverse shell on 8888 -> jabberwock
Reverse shel on 9999 [AFTER REBOOT] --> tweedledum
```

The password for humptydumpty didnt work but running `sudo -l` give us 
```
(tweedledee) NOPASSWD: /bin/bash
```

so lets log on as `tweedledee`

Seems like `tweedledee` have the same sudo permission for `tweedledum`

We have the same `humptydumpty.txt` file in the home directory..

We also have a `.gnupg` folder. I poked around at the 2 files there but couln't get anywhere..


Sooooo... im stupid.. I tried to log in to humptydumpty via ssh which didnt work... but simply `su` into it did work

From previous exploration, we knew that `humptydumpty` has access to `/home/alice/.ssh/id_rsa`

We retrieve the key from there and login via ssh using the key to `alice`

We can't run `sudo -l` since we don't have the password.

Soooo, after a lot of time poking around, I decided to have a look at some write ups.

I learned that you can have a look at `/etc/sudoers.d/*`  to get the sudo infos without `sudo -l` and without password

In our case the content of `/etc/sudoers.d/alice` was
```
alice ssalg-gnikool = (root) NOPASSWD: /bin/bash
```

I also didn't know that you could specify a hostname in sudoers.

In order for this to work, we need to specify the correct host with
```
sudo -h ssalg-gnikool /bin/bash
```

And we are root


Root flag
```
thm{bc2337b6f97d057b01da718ced6ead3f}
```