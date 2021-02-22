import json

CERES_HOME      = 'ceres_home'
DATA_ENCODING   = 'utf-8'
MAX_GROUPS      = 32
MAX_BLOCKS      = 8
BLOCK_SIZE      = 65536
INSERT_STRATEGY = "first"
SERVER_PORT     = 9001
SERVER_DEBUG    = True
SCHEMA          = {}


def init_schema():
    global SCHEMA
    global CERES_HOME
    try:
        with open(CERES_HOME + '/config/schema.json') as f:
            SCHEMA = json.load(f)
    except:
        raise ValueError("Schema load failed")