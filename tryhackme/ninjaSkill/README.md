# Tryhackme.com Room : Ninja Skill
`https://tryhackme.com/room/ninjaskills`


# Instance
```
export IP=10.10.43.125
```

# Nmap
```

```

```
8V2L
bny0
c4ZX
D8B3
FHl1
oiMO
PFbD
rmfX
SRSq
uqyw
v2Vb
X1Uy
```

We can `find / | grep {Name}` to get them.

We write a little script
```bash
#!/bin/bash
declare -a files=("8V2L" "bny0" "c4ZX" "D8B3" "FHl1" "oiMO" "PFbD" "rmfX" "SRSq" "uqyw" "v2Vb" "X1Uy")

for file in "${files[@]}";do
	grep "$file" find.txt >> out.txt
done

echo "Done"
cat out.txt
```

And find
```
/etc/8V2L
/mnt/c4ZX
/mnt/D8B3
/var/FHl1
/opt/oiMO
/opt/PFbD
/media/rmfX
/etc/ssh/SRSq
/var/log/uqyw
/home/v2Vb
/X1Uy
```

I got tired of the web console pretty quickly... Couldn't get a reverse shell... Since we're just dealing with files here, I just
```
cd / && python -m SimpleHTTPServer
```

And browse the server using a webbrowser.
And I downloaded every files

Im missing this file `bny0`.

Let's check the questions anyways.

# Task 1

1. Which of the above files are owned by the best-group group(enter the answer separated by spaces in alphabetical order)

We go back to the web console and run `find / -group best-user` and find
```
/mnt/D8B3
/home/v2Vb
```

The answer is
```
D8B3 v2Vb
```

2. Which of these files contain an IP address ?

We run `grep -R -n "[0-9]*\.[0-9]*\.*" .` and get :
```
./oiMO:43:wNXbEERat4wE0w/O9Mn1.1.1.1VeiSLv47L4B2Mxy3M0XbCYVf9TSJeg905weaIk
```

The answer is 
```
oiMO
```

3. Which file has the SHA1 hash of 9d54da7584015647ba052173b84d45e8007eba94

We run `sha1sum * | grep 9d54da7584015647ba052173b84d45e8007eba94`
```
9d54da7584015647ba052173b84d45e8007eba94  c4ZX
```

The answer is 
```
c4ZX
```

4. 	Which file contains 230 lines?

We run 	`wc -l *`

```
209 8V2L
209 c4ZX
209 D8B3
209 FHl1
209 oiMO
209 PFbD
209 rmfX
209 SRSq
209 uqyw
209 v2Vb
209 X1Uy
```

It's not there, an we are missing the `bny0` so i guess it's the answer
```
bny0
```

So here is another way to get all the paths to file
```
find / 2>/dev/null | grep '8V2L|bny0|c4ZX|D8B3|FHl1|oiMO|PFbD|rmfX|SRSq|uqyw|v2Vb|X1Uy'
```

We use `ls -n` to get the listing with user id
```
find / 2>/dev/null | grep '8V2L|bny0|c4ZX|D8B3|FHl1|oiMO|PFbD|rmfX|SRSq|uqyw|v2Vb|X1Uy' | while read line;do ls -n $line;done
```

We find that only /X1Uy belong to user 502

5. Which file's owner has an ID of 502?
```
X1Uy
```

From previous command we get the answer to question 6
```
/etc/8V2l
```

6. Which file is executable by everyone?
```
8V2L
```
