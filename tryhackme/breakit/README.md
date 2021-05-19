# Tryhackme.com Room : Break it

`https://tryhackme.com/room/breakit`



In this room, we are simply asked to 

"break" some "encryption/encoding".



Let's fire `cyberchef` and get started.



## Bases

The first encoded string is `MVQXG6K7MJQXGZJTGI======`

Which is `base32` for :

```
easy_base32
```



Then we have `TVJYWEtZVE1NVlBXRVlMVE1WWlE9PT09`

Which is `base64` followed by `base32` :

```
double_bases
```



Then we have `GM4HOU3VHBAW6OKNJJFW6SS2IZ3VAMTYORFDMUC2G44EQULIJI3WIVRUMNCWI6KGK5XEKZDTN5YU2RT2MR3E45KKI5TXSOJTKZJTC4KRKFDWKZTZOF3TORJTGZTXGNKCOE======`

Which is `base32` -> `base58` -> `from hex (base 16)` -> `base64`

```
base16_is_hex
```



Then we have `HRBUGQDUHFWDIXKUIBWXIJTHIE3DCY3BIE2FKQSZHNDE6MRUIA2TWWDMHRBV2ZKCHQWFCTLPIE2EEJDBIBZCEW3OHUSTOLRCHNFGMVC6IFJXIQ2AHVMVONSBHVOVIM2MHVPV42J4HQVCQ4REIFHVIJ2WHFWDYQSUHROGILJCIFIU23CXHNCEIXK2HRDVSXKOHV2SQJLC`



This one was a bit more tricky. My problem was not recognizing `base85` inputs an disregarding it as junk..

Our recipe is 

`base32` -> `base85` -> `base64` -> `base58` -> `base85` -> `base64` -> `base64`

```
that_is_a_lot_of_bases
```



Then we have this huge blob of text (Won't paste it here).

I had trouble with this one. Did take a look at a write up.

In the end, this is the solution :

`base32` -> `base85` -> `From decimal (Base 10)` -> `From Hex (Base 16)` -> `Base91` -> `Base58` ->  `From hex (Base 16)` -> `Base64` -> `From Decimal (Base 10)` -> `From hex (Base 16)` 

We get :

```
defense_the_base
```



## Base and Ciphers

We have ` PJXHQ4S7GEZV6ZTDOZQQ====`

Which is `base32` -> `Rot13`

```
make_13_spin
```

