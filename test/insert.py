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
    'level': sys.argv[2],
    "timestamp": "20210201T00:00:00"
}
data = {
    'messages': [message]
}

requests.post('http://localhost:9090/insert', json=data, headers=headers)
