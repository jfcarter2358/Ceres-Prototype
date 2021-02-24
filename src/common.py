import json
import configparser

CERES_HOME      = None
DATA_ENCODING   = None
MAX_GROUPS      = None
MAX_BLOCKS      = None
BLOCK_SIZE      = None
INSERT_STRATEGY = None
SERVER_PORT     = None
SERVER_DEBUG    = None
SCHEMA          = None

def read_config(config_path):
    global CERES_HOME
    global DATA_ENCODING
    global MAX_BLOCKS
    global MAX_GROUPS
    global BLOCK_SIZE
    global INSERT_STRATEGY
    global SERVER_DEBUG
    global SERVER_PORT

    config = configparser.ConfigParser()
    config.read(config_path)

    CERES_HOME = config['FILE_SYSTEM']['ceres_home']

    DATA_ENCODING   = config['DATA']['data_encoding']
    MAX_BLOCKS      = int(config['DATA']['max_blocks'])
    MAX_GROUPS      = int(config['DATA']['max_groups'])
    BLOCK_SIZE      = int(config['DATA']['block_size'])
    INSERT_STRATEGY = config['DATA']['insert_strategy']

    SERVER_DEBUG = config['SERVER'].getboolean('server_debug')
    SERVER_PORT  = int(config['SERVER']['server_port'])

    if CERES_HOME == None:
        raise ValueError("Configuration CERES_HOME not set")
    if DATA_ENCODING == None:
        raise ValueError("Configuration DATA_ENCODING not set")
    if MAX_BLOCKS == None:
        raise ValueError("Configuration MAX_BLOCKS not set")
    if MAX_GROUPS == None:
        raise ValueError("Configuration MAX_GROUPS not set")
    if BLOCK_SIZE == None:
        raise ValueError("Configuration BLOCK_SIZE not set")
    if INSERT_STRATEGY == None:
        raise ValueError("Configuration INSERT_STRATEGY not set")
    if SERVER_DEBUG == None:
        raise ValueError("Configuration SERVER_DEBUG not set")
    if SERVER_PORT == None:
        raise ValueError("Configuration SERVER_PORT not set")

def init_schema():
    global SCHEMA
    global CERES_HOME
    try:
        with open(CERES_HOME + '/config/schema.json') as f:
            SCHEMA = json.load(f)
    except:
        raise ValueError("Schema load failed")