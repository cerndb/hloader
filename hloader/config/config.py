print("loaded configuration module")

from ConfigParser import SafeConfigParser
CONFIG_FILES = ['hloader/config/config.ini']
CONFIG_PARSER = SafeConfigParser()
CONFIG_FILES_FOUND = CONFIG_PARSER.read(CONFIG_FILES)

CONFIG_FILES_MISSING = set(CONFIG_FILES) - set(CONFIG_FILES_FOUND)

print("Found config files:", sorted(CONFIG_FILES_FOUND))
print("Missing files     :", sorted(CONFIG_FILES_MISSING))


if len(CONFIG_FILES_FOUND) != 1:
    raise ValueError, "Failed to open/find all files"

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
