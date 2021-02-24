import requests
from datetime import datetime
import time
import sys

headers = {
    'Content-Type': 'application/json'
}

now = datetime.now()
message = {
    'year': now.year,
    'month': now.month,
    'day': now.day,
    'hour': now.hour,
    'minute': now.minute,
    'second': now.second,
    'service': 'foobar',
    'message': sys.argv[1],
    'level': sys.argv[2]
}
data = {
    'messages': [message]
}

requests.post('http://localhost:9001/insert', json=data, headers=headers)
