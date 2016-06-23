"""Configuration module"""
try:
    import configparser
except ImportError:
    import ConfigParser as configparser

import os

#for db connectors
print("loaded configuration module")

CONFIG_FILES = eval(os.getenv('HL_CONFIG_FILE',str([os.path.dirname(os.path.abspath(__file__))+'/config.ini'])))
CONFIG_PARSER = configparser.ConfigParser()
CONFIG_FILES_FOUND = CONFIG_PARSER.read(CONFIG_FILES)

CONFIG_FILES_MISSING = set(CONFIG_FILES) - set(CONFIG_FILES_FOUND)

print("Found config files:", sorted(CONFIG_FILES_FOUND))
if CONFIG_FILES_MISSING:
    print("Missing files     :", sorted(CONFIG_FILES_MISSING))

if len(CONFIG_FILES_FOUND) != 1:
    raise ValueError("Failed to open/find all files")

AUTH_ADDRESS = CONFIG_PARSER.get('default', 'AUTH_ADDRESS')
AUTH_PORT = CONFIG_PARSER.get('default', 'AUTH_PORT')
AUTH_USERNAME = CONFIG_PARSER.get('default', 'AUTH_USERNAME')
AUTH_PASSWORD = CONFIG_PARSER.get('default', 'AUTH_PASSWORD')
AUTH_SERVICE_NAME = CONFIG_PARSER.get('default', 'AUTH_SERVICE_NAME')
AUTH_TABLE = CONFIG_PARSER.get('default', 'AUTH_TABLE')
AUTH_USERNAME_ATTR = CONFIG_PARSER.get('default', 'AUTH_USERNAME_ATTR')
AUTH_DATABASE_ATTR = CONFIG_PARSER.get('default', 'AUTH_DATABASE_ATTR')
AUTH_SCHEMA_ATTR = CONFIG_PARSER.get('default', 'AUTH_SCHEMA_ATTR')
DEBUG = CONFIG_PARSER.get('default', 'DEBUG')
CLUSTER_BASE_PATH = CONFIG_PARSER.get('default', 'CLUSTER_BASE_PATH')
POSTGRE_ADDRESS = CONFIG_PARSER.get('default', 'POSTGRE_ADDRESS')
POSTGRE_PORT = CONFIG_PARSER.get('default', 'POSTGRE_PORT')
POSTGRE_USERNAME = CONFIG_PARSER.get('default', 'POSTGRE_USERNAME')
POSTGRE_PASSWORD = CONFIG_PARSER.get('default', 'POSTGRE_PASSWORD')
POSTGRE_DATABASE = CONFIG_PARSER.get('default', 'POSTGRE_DATABASE')
