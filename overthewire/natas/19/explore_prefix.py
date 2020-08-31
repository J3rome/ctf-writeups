import json
from collections import defaultdict

with open('prefixes.json', 'r') as f:
    prefixes = json.load(f)

second_pos = defaultdict(list)
for p in prefixes:
    print(f"{p} -- {p[1]}")
    second_pos[p[1]].append(p)

#print(json.dumps(second_pos))

