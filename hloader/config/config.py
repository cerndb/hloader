print("loaded configuration module")

from ConfigParser import SafeConfigParser
files = ['hloader/config/config.ini']
parser = SafeConfigParser()
found = parser.read(files)

missing = set(files) - set(found)

print("Found config files:", sorted(found))
print("Missing files     :", sorted(missing))


if len(found) != 1:
    raise ValueError, "Failed to open/find all files"

AUTH_TABLE = parser.get('default', 'AUTH_TABLE')
AUTH_USERNAME_ATTR = parser.get('default', 'AUTH_USERNAME_ATTR')
AUTH_DATABASE_ATTR = parser.get('default', 'AUTH_DATABASE_ATTR')
AUTH_SCHEMA_ATTR = parser.get('default', 'AUTH_SCHEMA_ATTR')
DEBUG = parser.get('default', 'DEBUG')
CLUSTER_BASE_PATH = parser.get('default', 'CLUSTER_BASE_PATH')
POSTGRE_ADDRESS = parser.get('default', 'POSTGRE_ADDRESS')
POSTGRE_PORT = parser.get('default', 'POSTGRE_PORT')
POSTGRE_USERNAME = parser.get('default', 'POSTGRE_USERNAME')
POSTGRE_PASSWORD = parser.get('default', 'POSTGRE_PASSWORD')
POSTGRE_DATABASE = parser.get('default', 'POSTGRE_DATABASE')
