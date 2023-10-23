import requests
import json
import time

url = "http://127.0.0.1:8000/api/files/"
file = {'file': open('test.text', 'rb')}
data = {'ttl': 2}

r = requests.post(url, files=file, data=data)

# Print response message
print(json.dumps(r.json(), indent=4))

key = r.json()['key']

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

