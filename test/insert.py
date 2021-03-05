import requests
from datetime import datetime
import time
import sys

headers = {
    'Content-Type': 'application/json'
}

now = datetime.now()
'''
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
'''
message1 = {
    'day': 5, 
    'hour': 22, 
    'level': 'ERROR', 
    'message': '[2021-03-05T22:50:20] [model-manage] [<span class="ERROR">ERROR</span>] [c.o.m.m.EurekaServiceMonitor] Failed to properly check/update service engine-test: [500 Internal Server Error] during [GET] to [http://gateway:8090/engine-test/1/health] [EngineApiV2Client#getHealthCheck(String)]: [{"timestamp":"2021-03-05T22:50:20.653+0000","path":"/engine-test/1/health","status":500,"error":"Internal Server Error","message":"Connection prematurely closed BEFORE response","requestId":"147c44cb"}]', 
    'minute': 50, 
    'month': 3, 
    'second': 20, 
    'service': 'model-manage', 
    'timestamp': '2021-03-05T22:50:20', 
    'year': 2021
}
message2 = {
    'day': 5, 
    'hour': 22, 
    'level': 'INFO', 
    'message': '[2021-03-05T22:50:20] [model-manage] [<span class="ERROR">ERROR</span>] [c.o.m.m.EurekaServiceMonitor] Failed to properly check/update service engine-test: [500 Internal Server Error] during [GET] to [http://gateway:8090/engine-test/1/health] [EngineApiV2Client#getHealthCheck(String)]: [{"timestamp":"2021-03-05T22:50:20.653+0000","path":"/engine-test/1/health","status":500,"error":"Internal Server Error","message":"Connection prematurely closed BEFORE response","requestId":"147c44cb"}]', 
    'minute': 50, 
    'month': 3, 
    'second': 20, 
    'service': 'model-manage', 
    'timestamp': '2021-03-05T22:50:20', 
    'year': 2021
}
data = {
    'messages': [message1, message2]
}

requests.post('http://localhost:9090/insert', json=data, headers=headers)
