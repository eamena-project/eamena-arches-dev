#!/usr/bin/python3

import json, sys

if len(sys.argv) <= 1:
        sys.stderr.write("Usage: jsonl2json.py [jsonl_file]\n")
        sys.exit(1)

filename = sys.argv[1]

fp = open(filename, 'r')
ret = {"business_data": {"resources": []}}
while True:

        jsondata = fp.readline()
        if(jsondata == ''):
                break

        ret['business_data']['resources'].append(json.loads(jsondata))

fp.close()

print(json.dumps(ret))
