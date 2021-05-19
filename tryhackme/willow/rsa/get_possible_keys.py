from math import gcd

p = 11
q = 13

n = q * p
phi = (q-1) * (p-1)

possible_encryption_keys = []

for i in range(2, phi):
    if gcd(n, i) == 1 and gcd(phi, i) == 1:
        possible_encryption_keys.append(i)

e = possible_encryption_keys[0]

possible_decryption_keys = []

for i in range(phi + 1, phi + 1000):
    if i * e % phi == 1:
        possible_decryption_keys.append(i)

d = possible_decryption_keys[0]


print("Public key = (", e, ", ", n, ")")
print("Private key = (", d, ", ", n, ")")

to_encrypt = "Hello World"

encrypted = ""
for c in to_encrypt:
    encrypted += chr((ord(c)**e) % n)

print("")
print("To encrypt : ", to_encrypt)
print("Encrypted : ", encrypted)

decrypted = ""
for c in encrypted:
    decrypted += chr((ord(c)**d) % n)

print("Decrypted : ", decrypted)


