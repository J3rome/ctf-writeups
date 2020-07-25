# Tryhackme.com Room : Pinux Privesc Playground
`https://tryhackme.com/room/privescplayground`


# Instance
```
export IP=10.10.197.22
```

This is a cool little playground with a LOT of vulnerabilities.

We run `sudo -l` and get :
```
(root) NOPASSWD: /bin/apt-get*
 (root) /bin/apt*
 (root) /usr/bin/aria2c
 (root) /usr/sbin/arp
 (root) /bin/ash
 (root) /usr/bin/awk
 (root) /usr/bin/base64
 (root) /bin/bash
 (root) /bin/busybox
 (root) /bin/cat
 (root) /bin/chmod
 (root) /bin/chown
 (root) /bin/cp
 (root) /usr/bin/cpan
 (root) /usr/bin/cpulimit
 (root) /bin/crontab
 (root) /bin/csh
 (root) /bin/curl
 (root) /usr/bin/cut
 (root) /bin/dash
 (root) /bin/date
 (root) /bin/dd
 (root) /usr/bin/diff
 (root) /bin/dmesg
 (root) /sbin/dmsetup
 (root) /usr/bin/docker
 (root) /usr/bin/dpkg
 (root) /usr/bin/easy_install
 (root) /usr/bin/emacs
 (root) /usr/bin/env
 (root) /usr/bin/expand
 (root) /usr/bin/expect
 (root) /usr/bin/facter
 (root) /usr/bin/file
 (root) /usr/bin/find
 (root) /usr/bin/flock
 (root) /usr/bin/fmt
 (root) /usr/bin/fold
 (root) /usr/bin/ftp
 (root) /usr/bin/gawk
 (root) /usr/bin/gdb
 (root) /usr/bin/gimp
 (root) /usr/bin/git
 (root) /bin/grep
 (root) /usr/bin/head
 (root) /usr/sbin/iftop
 (root) /usr/bin/ionice
 (root) /sbin/ip
 (root) /usr/bin/irb
 (root) /usr/bin/jq
 (root) /usr/bin/ksh
 (root) /sbin/ldconfig
 (root) /usr/bin/less
 (root) /sbin/logsave
 (root) /usr/bin/ltrace
 (root) /usr/bin/lua
 (root) /usr/bin/make
 (root) /usr/bin/man
 (root) /usr/bin/mawk
 (root) /bin/more
 (root) /bin/mount
 (root) /usr/bin/mtr
 (root) /bin/mv
 (root) /usr/bin/nano
 (root) /usr/bin/nawk
 (root) /bin/nc
 (root) /usr/bin/nice
 (root) /usr/bin/nl
 (root) /usr/bin/nmap
 (root) /usr/sbin/node
 (root) /usr/bin/od
 (root) /usr/bin/openssl
 (root) /usr/bin/perl
 (root) /usr/bin/pg
 (root) /usr/bin/php
 (root) /usr/bin/pic
 (root) /usr/bin/pico
 (root) /usr/bin/pip
 (root) /usr/bin/puppet
 (root) /usr/bin/python
 (root) /usr/bin/readelf
 (root) /usr/bin/redm
 (root) /usr/bin/rlwrap
 (root) /usr/bin/rsync
 (root) /usr/bin/ruby
 (root) /usr/bin/run-mailcaps
 (root) /bin/run-parts
 (root) /usr/bin/rvim
 (root) /usr/bin/scp
 (root) /usr/bin/screen
 (root) /usr/bin/script
 (root) /bin/sed
 (root) /usr/sbin/service
 (root) /usr/bin/setarch
 (root) /usr/bin/sftp
 (root) /usr/bin/smbclient
 (root) /usr/bin/socat
 (root) /usr/bin/sort
 (root) /usr/bin/sqlite3
 (root) /usr/bin/ssh
 (root) /sbin/start-stop-daemon
 (root) /usr/bin/stdbuf
 (root) /usr/bin/strace
 (root) /usr/bin/tail
 (root) /bin/tar
 (root) /usr/bin/taskset
 (root) /usr/bin/tclsh
 (root) /usr/sbin/tcpdump
 (root) /usr/bin/tee
 (root) /usr/bin/telnet
 (root) /usr/bin/tftp
 (root) /usr/bin/time
 (root) /usr/bin/timeout
 (root) /usr/bin/tmux
 (root) /usr/bin/ul
 (root) /usr/bin/unexpand
 (root) /usr/bin/uniq
 (root) /usr/bin/unshare
 (root) /usr/bin/vi
 (root) /usr/bin/vim
 (root) /usr/bin/watch
 (root) /usr/bin/wget
 (root) /usr/bin/xargs
 (root) /usr/bin/xxd
 (root) /usr/bin/zip
 (root) /usr/bin/zsh
 ```

That's a lot of sudo binaries.. The easiest is to spawn another shell like `bash`,`dash` or `zsh`, `ash`, `csh`, `tmux`, `busybox`, `screen`, `ruby`, `python`, `php`, `perl`

There is alot of other binarie that we can abuse to read/write root file or get shell access.

We can easily get the flag in `/root/flag.txt`
```
THM{3asy_f14g_1m40}
```

We can find setuid binaries `find / -perm -4000 2>/dev/null`
```
/usr/sbin/arp
/usr/sbin/node
/usr/sbin/uuidd
/usr/sbin/pppd
/usr/lib/eject/dmcrypt-get-device
/usr/lib/pt_chown
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/openssh/ssh-keysign
/usr/bin/wget
/usr/bin/cut
/usr/bin/base64
/usr/bin/traceroute6.iputils
/usr/bin/tail
/usr/bin/aria2c
/usr/bin/ul
/usr/bin/shuf
/usr/bin/php5
/usr/bin/gpasswd
/usr/bin/make
/usr/bin/openssl
/usr/bin/file
/usr/bin/tclsh8.5
/usr/bin/env
/usr/bin/diff
/usr/bin/watch
/usr/bin/strace
/usr/bin/rlwrap
/usr/bin/expand
/usr/bin/fold
/usr/bin/vim.basic
/usr/bin/timeout
/usr/bin/xargs
/usr/bin/expect
/usr/bin/chsh
/usr/bin/jq
/usr/bin/perl5.14.2
/usr/bin/readelf
/usr/bin/sudo
/usr/bin/ionice
/usr/bin/sudoedit
/usr/bin/unshare
/usr/bin/time
/usr/bin/taskset
/usr/bin/mtr
/usr/bin/emacs23-x
/usr/bin/flock
/usr/bin/tee
/usr/bin/xxd
/usr/bin/setarch
/usr/bin/python2.7
/usr/bin/uniq
/usr/bin/head
/usr/bin/sort
/usr/bin/newgrp
/usr/bin/stdbuf
/usr/bin/at
/usr/bin/nl
/usr/bin/perl
/usr/bin/tftp
/usr/bin/find
/usr/bin/passwd
/usr/bin/rsync
/usr/bin/docker
/usr/bin/pg
/usr/bin/fmt
/usr/bin/nice
/usr/bin/od
/usr/bin/chfn
/usr/bin/gimp-2.6
/usr/bin/gdb
/usr/bin/unexpand
/sbin/dmsetup
/sbin/start-stop-daemon
/sbin/logsave
/bin/sed
/bin/mount
/bin/mv
/bin/cp
/bin/dash
/bin/ksh93
/bin/chmod
/bin/ping
/bin/chown
/bin/fusermount
/bin/bash
/bin/nano
/bin/ip
/bin/more
/bin/cat
/bin/zsh4
/bin/less
/bin/su
/bin/busybox
/bin/dd
/bin/grep
/bin/run-parts
/bin/ping6
/bin/date
/bin/bsd-csh
/bin/umount
```

Wow.. A lot of binaries and a lot that are super easy to exploit.