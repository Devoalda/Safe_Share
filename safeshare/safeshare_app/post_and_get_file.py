import requests
import json
import time

url = "http://127.0.0.1:8000/api/files/"

# Send test.text and test2.text to server as a list
files = [('file', open('test.text', 'rb')), ('file', open('test2.text', 'rb'))]
data = {'ttl': 2}

r = requests.post(url, files=files, data=data)

# Print response message
print(json.dumps(r.json(), indent=4))

for msg in r.json():
    print(msg['key'])
    print(msg['msg'])
    key = msg['key']

# Wait for file to expire
time.sleep(3)

url = "http://127.0.0.1:8000/api/files/" + key + "/"
r = requests.get(url)

# Print response message
print(json.dumps(r.json(), indent=4))

if r.json()['file'] is not None:
    file = r.json()['file']
# Change file to bytes
    file = bytes(file, 'utf-8')

# Write response('file') to disk
    with open('test2.text', 'wb') as f:
        f.write(file)

