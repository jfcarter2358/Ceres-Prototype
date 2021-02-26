import common
import exporter
import importer
import manager
import antler
import os
import sys
import time
from flask_api import FlaskAPI
from flask import request
from flask_api import status
import json
from datetime import datetime
import utils

free_data = {}
app = FlaskAPI(__name__)

def _init_free():
    global free_data

    if os.path.exists('{}/data/free_data.json'.format(common.CERES_HOME)):
        with open('{}/data/free_data.json'.format(common.CERES_HOME)) as f:
            free_data = json.load(f)
    else:
        for i in range(0, common.MAX_GROUPS):
            free_data[i] = {j:[{"start": 0, "end": 65536}] for j in range(0, common.MAX_BLOCKS)}

@app.route('/insert', methods=['POST'])
def post_message():
    global free_data

    data = request.get_json()
    start = time.time()
    idents = []

    for message in data['messages']:
        insert_string = ''
        meta = []
        for k in common.SCHEMA['order']:
            if common.SCHEMA['fields'][k] == 'str':
                insert_string += '{},'.format(message[k].replace(',', '<COMMA>'))
            else:
                insert_string += '{},'.format(message[k])
            if k != 'message':
                meta.append('{}/{}'.format(k, message[k]))
        
        insert_string = insert_string[:-1]
        free_data, ident = importer.get_writable(insert_string, free_data, meta)
        idents.append(ident)
    with open('{}/data/free_data.json'.format(common.CERES_HOME), 'w') as f:
        json.dump(free_data, f)

    end = time.time()

    return {'status': status.HTTP_200_OK, "ids": idents}

@app.route('/query', methods=['POST'])
def get_results():
    global free_data

    data = request.get_json()
    out = []
    query = data['query']
    start = time.time()
    idents, mode = antler.parse(query)
    if mode == 'select':
        for i in idents:
            data = exporter.get_data(i)
            out.append(utils.map_dict(data, i))
    elif mode == 'delete':
        for i in idents:
            free_data = manager.delete_data(i, free_data)
        free_data = manager.merge_free(free_data)
        with open('{}/data/free_data.json'.format(common.CERES_HOME), 'w') as f:
            json.dump(free_data, f)
    end = time.time()
    print('{}'.format(end - start))
    return {'status': status.HTTP_200_OK, "data": out}

def _do_run():
    global app
    app.run(host='0.0.0.0', port=common.SERVER_PORT, debug=common.SERVER_DEBUG)

def _do_test():
    global free_data

    out = []

    counter = 0

    with open('test/logs.txt') as f:
        logs = f.read().split('\n')
    for l in logs:
        start = time.time()
        free_data, ident = importer.get_writable(l, free_data)
        end = time.time()
        print('{} : {}'.format(end - start, ident))
        out.append('{},{}'.format(counter, end - start))
    with open('timing.csv', 'w') as f:
        f.write('\n'.join(out))

    _do_run()
        
if __name__ == '__main__':
    config_path = os.getenv('CERES_CONFIG_PATH')
    if not config_path:
        config_path = 'ceres_home/config/config.ini'
    common.read_config(config_path)
    common.init_schema()
    _init_free()
    if sys.argv[1] == 'test':
        print('testing')
        _do_test()
    elif sys.argv[1] == 'run':
        print('running')
        _do_run()