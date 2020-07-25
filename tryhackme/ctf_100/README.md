# Tryhackme.com Room : CTF 100
`https://tryhackme.com/room/ctf100`


# Instance
```
export IP=10.10.151.5
```

# Nmap
`nmap -Pn -p- -v -T5 $IP`
```
PORT     STATE SERVICE
3333/tcp open  dec-notes
9999/tcp open  abyss
```

# Flag 1
Ok so we just `nc $IP 333` and get a prompt:
```
***************************
*   100 Flags challenge   *
***************************
Welcome to the THM point grabbing challenge!
The task is simple, find the flag and get the point
It can be hard or easy, IDK
To start the challenge, I need your address. So that I can send it to you.
```

Entering our machine IP we get :
```
Well done! Please take your first flag
flag 1: you_got_a_message
5 open ports is now opened for you! Hint: 4 digits and start with 3
Good luck!
```

So we got the first flag and there is 5 new ports open.
We nmap again with `nmap -Pn -p- -v -T5 $IP` and get :
```
3333/tcp open  dec-notes
3343/tcp open  ms-cluster-net
3353/tcp open  fatpipe
3363/tcp open  nati-vi-server
3373/tcp open  lavenir-lm
3383/tcp open  esp-lm
```

So seems like they are all port waiting for a netcat/telnet connection.

# Flag 2
`nc $IP 3343` give
```
Flag 2 challenge
Crack the following code
Guvf_vf_prnfre_pvcure
```

Look like ROT cipher, it is `ROT13` and we get :
```
This_is_ceaser_cipher
```

The text is not the flag. We get the flag by sending the decoded text to the same port :
```
> This_is_ceaser_cipher

Good job!
flag 2: qt8pm59jh5r49uqdwfw2
Just some numbering: 8989
```

tried to connect to `8989` port but couln't connect. we'll come back to it later

# Flag 3
`nc $IP 3353`:
```
Flag 3 challenge
Crack the following code
Kxydrob_mokcob_mszrob
```

Again ROT...`ROT10` :
```
Another_ceaser_cipher
```

We get :
```
> Another_ceaser_cipher

Good job!
flag 3: 5wdtc7jzk33qjauh5gxm
Just some numbering: 7431
```

# Flag 4
`nc $IP 3363` :
```
Flag 4 challenge
Crack the following code
where is the key
Ez_me_jnvrk_sb_fslv_afij
```

This is a vigenere cipher. This was a bit tricky, the key is `where`
We get:
```
> Is_in_front_of_your_eyes

Good job!
flag 4: sm8jvu8jxu7dz6s7qmsp
Just some numbering: 5667
```


# Flag 5
`nc $IP 3373` :
```
Flag 5 challenge
Crack the following code
-- --- .-. ... . / -.-. --- -.. . / -... . . .--. / -... --- --- .--.
```

This is morse, using cyberchef we find :
```
MORSECODEBEEPBOOP
```

This doesn't work tho, Looking at the hint, they mention the `/`.. It is actually a word delimiter so :

```
> MORSE CODE BEEP BOOP

Good job!
flag 5: 2p3363hrava9fbq296ca
Just some numbering: 9332
```


# Flag 6
`nc $IP 3383` :
```
Flag 6 challenge
Crack the following code
59 6f 75 20 67 65 74 20 68 65 78 2d 65 64
```

This is hex and we get :
```
You get hex-ed
```

We get :
```
Good job!
flag 6: skuj9359mqdm6sv8d8z6
Just some numbering: 3331
```

# Flag 7
We used up all the ports we had, tried all the `just some numbering` ports without success.

Let's try another nmap.
Hmm.. seems like we find the same ports open again.. No new ports...

Maybe if we send our ip to `:3333` again ?
Hmmm.. No luck

Ahh.. looking at the hint, it says that we have to connect to `:9999`.
We get :
```
***************************
*   Port knocking input   *
***************************
Hi user, please enter the port sequence
The format is (can be more than 4): PORT PORT PORT PORT
```

Let's try with the `just some numbering` numbers
```
> 8989 7431 5667 9332 3331
Something happen
Good luck!
```

Soo something happened... Still can't connect to `8989` but let's run a nmap scan again

Seems like one more port is open now `4000`.
When we connect to it we get :
```
Congratulation! You have captured all the flag
Please go home, nothing to see here
Type 'exit' and leave this place
WHY are you here? Leave
```

When i enter something i get :
```
Don't you try anything funny
One more try, kick you out
```

And then if I enter another command i'm getting kicked out...

Hmmm, what can we do ?
We could bruteforce this thing ?

Oh wellll.... Bruteforcing with rockyou, I found a strange behaviour when just sendinf a newline.

The first newline we get :
```
GET LOST!
```

Then the second
```
Please I beg you, LEAVE!
```

And finally the third :
```
Oh my fking god, take it, JUST TAKE IT
flag 7: zmht7gg3q3ft7cmc942n
Please leave, thank you
```

So let's run an nmap scan again i guess ?

Seems like we got new ports open :
```
4000/tcp open  remoteanything
4001/tcp open  newoak
4002/tcp open  mlchat-proxy
4003/tcp open  pxc-splr-ft
4004/tcp open  pxc-roid
4005/tcp open  pxc-pin
```

# Flag 8
`nc $IP 4001`:
```
Flag 8 challenge
Crack the following code
QSBjb21tb24gYmFzZQ==
```

this is base64, we get
```
> A common base

Good job!
flag 8: dmm32qvfkfwm6yjnw46k
Same old stuff: 10113
```

# Flag 9
`nc $IP 4002`:
```
Flag 9 challenge
Crack the following code
KRUGS4ZANFZSAYJAONWWC3DMMVZCAYTBONSQ====
```

Again base 64 ? Actually it is base32
```
> This is a smaller base

Good job!
flag 9: fuf8mx74nph26f69mr97
Same old stuff: 10415
```

# Flag 10
`nc $IP 4003`:
```
Flag 10 challenge
Crack the following code
4UFrmghikrDhdg9avkV9avpg4uHQmhvUf7GgRoCo
```

This is Base58 :
```
> Look like a brother to base64

Good job!
flag 10: hud9bm8yc37md5b7t7mn
Same old stuff: 21033
```

# Flag 11
`nc $IP 4004`:
```
Flag 11 challenge
Crack the following code
9lG&`+@/pn8P(%7BOPpi@ru:&
```

This is base85
```
> More ASCII character

Good job!
flag 11: 4xm43r2wajrsrbm4775d
Same old stuff: 35555
```

# Flag 12
`nc $IP 4005`:
```
Flag 12 challenge
Crack the following code
Erzg,W]@7RqSkb9jPD<:vz3B
```

This is base 91
```
> More and More ASCII

Good job!
flag 12: qtfvbd7gbvyg9gww5jwj
Same old stuff: 25637
```

# Flag 13
We now need more ports so let's head to port `9999` and enter `10113 10415 21033 35555 25637`

But we get a wrong sequence... hmmmm

From the hint, we see that we need to reverse the order :
```
> 25637 35555 21033 10415 10113
Something happen
Good luck!
```

Let's Nmap again.

We find port `6000`
`nc $IP 6000` :
```
Congratulation on getting this far
You are a worthy challenger
5 more gates are opened for you
Take this as your reward
flag 13: aehg24vwn5yyc8jz4tv5
```

# Flag 14
Let's nmap again then...

We find :
```
6010/tcp open  x11
6020/tcp open  x11
6030/tcp open  x11
6040/tcp open  x11
6050/tcp open  arcserve
```

We `nc $IP 6010`:
```
Flag 14 challenge
Crack the following code
pi pi pi pi pi pi pi pi pi pi pika pipi pi pipi pi pi pi pipi pi pi pi pi pi pi pi pipi pi pi pi pi pi pi pi pi pi pi pichu pichu pichu pichu ka chu pipi pipi pipi pi pi pi pi pi pi pi pi pi pi pikachu pipi pi pi pi pi pi pikachu pi pi pikachu ka ka ka ka ka ka ka ka ka ka pikachu pi pi pikachu pi pi pi pi pi pikachu pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pichu pichu pi pi pikachu pipi pipi ka ka ka ka ka ka ka ka ka ka ka ka pikachu pi pi pi pi pi pi pi pi pi pi pikachu pichu pichu pikachu pipi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pi pikachu pichu pikachu pipi pipi pi pikachu pi pi pi pi pi pikachu ka ka ka ka ka ka ka ka ka pikachu pichu pi pi pi pi pikachu pichu pikachu pipi pipi ka pikachu pichu pi pikachu pichu pikachu pipi ka pikachu pipi ka ka ka pikachu pichu pikachu ka ka pikachu pipi pi pi pi pi pi pi pi pi pikachu ka ka pikachu pichu pi pi pi pi pi pi pikachu ka ka ka ka ka ka pikachu pichu pikachu pipi pipi ka ka pikachu ka pikachu ka ka ka ka pikachu pichu pi pi pikachu pipi pi pi pikachu pi pi pikachu ka pikachu
```

This is `pikalang` we execute using `https://www.dcode.fr/pikalang-language` and get
```
> Pikachu is a type of electric pokemon

Good job!
flag 14: k2phhw85emq3v4njj5g6
You know the drill: 31031
```

# Flag 15
`nc $IP 6020`
```
Flag 15 challenge
Crack the following code
000000000000000000000000000000110010000010000000000010000000000000000000000010000000000000000000000000000000011011011011001111010010010000000000000000000000000000000000000000000100010000000000000100000100000000000000000000000000000000100011011000000100010010001001001001001001001001001001100000000000000000000000000000000100011011100010010001001001001001100000100000000000000000100011011100010000000000000000000000000000000000000000100011100010000100000000000000000000000100000000000000000100001001001001001001001001001001001001001100010001001100000000000000000000000100
```

The hint says to look at esolang.

Potentials :
```
BCDFuck (Hex)
prelude (Hex)
Word!CPU (Hex)

Bitwise Cyclic tag
Whirl
```

Couldn't get any output for Bitwise Cyclic tag and whirl on `tio.run`

# Flag 16
`nc $IP 6030`
```
Flag 16 challenge
Crack the following code
111111111100100010101011101011111110101111111111011011011011000001101001001000101001011111111111001010111001010000000000000000000000001010011011110010100100100000000000000000000000000000000010101111111111111001010000000000000000000000000000000001010011011001010010010111111111111111001010000000000001010000001010001010000001010
```

Hmmm.. Again... similar to challenge 15

# Flag 17
`nc $IP 6040`
```
Flag 17 challenge
Crack the following code
----------]<-<---<-------<---------->>>>+[<<<------------,<-,-----------------,+++++++++++++++++,-------------,-,++++++++++++++,>>--,<<----------,+++++++++,>>,<<++++,----------------,>---------------,--------,<++++,>+++,<-------,>+++,--------,
```

# Flag 18
`nc $IP 6050`
```
Flag 18 challenge
Crack the following code
eeeeeeeeeepaeaeeeaeeeeeeeaeeeeeeeeeeccccisaaaeeeejaeeeeeeeeeeeeeeeeejiijejcceejaaiiiiiiiijiiijeejiiiiiijccjaaeeeeeeeeeeeeeeejiiiiiiiiiiiijiiijccjaaiiijeeeeeeeeeeeeeeeejiiiiiiiiiiiiiiiiijeeeeeeeejeeeeejiiiiiiiijeeeeeeeeeeeeeeejiiiiiiiiiiiiiiiiiijeeeeeeeej
```

