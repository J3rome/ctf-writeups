import pexpect

p = pexpect.spawn('/bin/sh', encoding='utf-8')
p.expect('$')

