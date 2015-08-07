from pass_config import POSTGRE_ADDRESS, POSTGRE_DATABASE, POSTGRE_PORT, POSTGRE_USERNAME, POSTGRE_PASSWORD, \
    ORACLE_ALIAS, ORACLE_PORT, ORACLE_USERNAME, ORACLE_PASSWORD, ORACLE_SID, \
    AUTH_ALIAS, AUTH_PORT, AUTH_USERNAME, AUTH_PASSWORD, AUTH_SID

AUTH_TABLE = 'hadoop_data_integrator.accounts_info'
AUTH_USERNAME_ATTR = 'owner_login'
AUTH_DATABASE_ATTR = 'database_name'
AUTH_SCHEMA_ATTR = 'login'

DEBUG = False
