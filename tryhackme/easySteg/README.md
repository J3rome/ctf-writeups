# Tryhackme.com Room : Easy Steganography
`https://tryhackme.com/room/easysteganography`

So we get an archive with 4 jpg files.

Running `binwalk flag1.jpg` we get:
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, EXIF standard
12            0xC             TIFF image data, little-endian offset of first image directory: 8
270           0x10E           Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stRef=
```

`binwalk -e` didn't give anything, had to do `binwalk --dd=".*" flag1.jpeg` to extract data

Doesn't seems to be anything good in there.

`binwalk flag2.jpeg` give us 
```
DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, EXIF standard
12            0xC             TIFF image data, little-endian offset of first image directory: 8
270           0x10E           Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stRef=
78447         0x1326F         JPEG image data, JFIF standard 1.01
```

There is another image in there. Maybe we need to crack the passphrase of this image ?


Running strings on `flag3.jpeg` give us :
```
The passphrase to this challenge is Math
```
Tried steghide on it but didn't work, maybe it's the passphrase for another image?
Can't see nothing else in the file using `binwalk`.


`binwalk flag4.jpeg` give us:
```
0             0x0             JPEG image data, EXIF standard
12            0xC             TIFF image data, little-endian offset of first image directory: 8
270           0x10E           Unix path: /www.w3.org/1999/02/22-rdf-syntax-ns#"> <rdf:Description rdf:about="" xmlns:xmpMM="http://ns.adobe.com/xap/1.0/mm/" xmlns:stRef=
78447         0x1326F         XML document, version: "1.0"
```

Let's check that XML. Hmmm can't find anything in there... May be related to LibreOffice ?

We find this string also
```
TryHardered
```

Sooo, not used to steg, couldn't get further. decided to lookup the writeup.

The flag can actually be dumped with `strings`. There is no default flag format but we know that our flag has 7 characters. we can `strings flag1.jpeg | perl -lne 'length() == 7 && print'`. Manually looking through the output we find the first flag :
```
St3g4n0
```

Let's try the same with flag2. The flag is 9 characters `strings flag2.jpeg | perl -lne 'length() == 9 && print'`

Nopp can't find anything.

oH well, eralier we extracted a second image from `flag2.jpeg` using `binwalk`. Well, the flag is simply the text written in the image :
```
ALGORITHM
```

Oh welll... Again, for flag 3, was looking for something more difficult. The flag is actually the string that we found. thought it was a passphrase for steghide.
```
The passphrase to this challenge is Math
```

So the flag is
```
Math
```

Again, was looking too far for the flag. We actually already found the flag for `flag4.jpeg` it was 
```
TryHardered
```