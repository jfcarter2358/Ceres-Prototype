import requests
from datetime import datetime
import time


headers = {
    'Content-Type': 'application/json'
}

with open('test/logs.txt', 'r') as f:
    logs = f.read().split('\n')

levels = ['INFO', 'WARN', 'DEBUG', 'ERROR', 'TRACE']

messages = []
for i in range(0, len(logs)):
    if i % 100 == 0:
        print('{} of {}'.format(i, len(logs)))
        data = {
            'messages': messages
        }

        requests.post('http://localhost:9090/insert', json=data, headers=headers)
        messages = []
    now = datetime.now()
    message = {
        'year': now.year,
        'month': now.month,
        'day': now.day,
        'hour': now.hour,
        'minute': now.minute,
        'second': now.second,
        'service': 'foobar',
        'message': logs[i],
        'level': levels[i % 5]
    }
    time.sleep(0.001)
    messages.append(message)