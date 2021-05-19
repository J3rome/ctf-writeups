var serialize = require('node-serialize');

var input = process.argv[2]

var decoded = Buffer.from(input, 'base64').toString('ascii')

var unserialized = serialize.unserialize(decoded)

console.log(unserialized)
