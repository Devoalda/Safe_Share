import requests
import json

url = "http://127.0.0.1:8000/api/files/"
file = {'file': open('test.text', 'rb')}

r = requests.post(url, files=file)

# Print response message
print(json.dumps(r.json(), indent=4))

key = r.json()['key']

url = "http://127.0.0.1:8000/api/files/" + key + "/"
r = requests.get(url)

file = r.json()['file']
# Change file to bytes
file = bytes(file, 'utf-8')

# Write response('file') to disk
with open('test2.text', 'wb') as f:
    f.write(file)
