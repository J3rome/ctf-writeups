# Over The Wire -- Natas 19

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

Running the search in parallel would definitely be more efficient