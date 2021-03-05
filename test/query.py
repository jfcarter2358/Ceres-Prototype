import requests
import sys

query = sys.argv[1]

headers = {
    'Content-Type': 'application/json'
}

data = {
    'query': query
}

r = requests.post('http://localhost:9090/query', json=data, headers=headers)
print(r.content)