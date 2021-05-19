import string
import itertools

word_len = 3

comb = itertools.product(string.ascii_lowercase, repeat=word_len)

for c in comb:
    print("".join(c))

        
