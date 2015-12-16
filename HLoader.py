import argparse
import sys
from os import environ

from hloader.db.DatabaseManager import DatabaseManager
from runserver import RunAPIServer

###############################################################################
#                           argparse configuration                            #
###############################################################################

parser = argparse.ArgumentParser(description='CERN HLoader')

parser.add_argument('-c', '--check-sanity', action='store_true', help='Check the sanity of the execution environment')
parser.add_argument('-r', '--run', help='Run the Flask microserver', action='store_true')
parser.add_argument('--debug', help='Enable debugging mode', action='store_true', default=False)
parser.add_argument('--use-reloader', action='store_true', help='Use reloader to run Flask microserver', default=False)
parser.add_argument('--oracledb-url', action='store', help='Specify Oracle DB URL')
parser.add_argument('--postgres-host', action='store', help='Specify PostgreSQL host', default='localhost')
parser.add_argument('--postgres-dbname', action='store', help='Specify PostgreSQL database name', default='hloader')
parser.add_argument('--postgres-port', action='store', help='Specify PostgreSQL port number', default='5432')
parser.add_argument('--postgres-user', action='store', help='Specify PostgreSQL username', default='hloader')
parser.add_argument('--postgres-password', action='store', help='Specify PostgreSQL password')

args = vars(parser.parse_args())


if len(sys.argv) == 1:
    # Load configuration
    # Initialize database connection
    # Initialize scheduler
    # Start transfers

    # Load configuration

    # Initialize database connection
    DBM = DatabaseManager()

    postgre_address = environ.get('POSTGRE_ADDRESS')
    postgre_port = environ.get('POSTGRE_PORT')
    postgre_username = environ.get('POSTGRE_USERNAME')
    postgre_password = environ.get('POSTGRE_PASSWORD')
    postgre_database = environ.get('POSTGRE_DATABASE')

    if not (postgre_address and postgre_port and postgre_username and postgre_password and postgre_database):
        raise Exception("Environmental variables are not properly set up.")

    DBM.connect_meta("PostgreSQLA", postgre_address, postgre_port, postgre_username, postgre_password, postgre_database)

    # Initialize scheduler

    # Start transfers

    RunAPIServer(debug=True, use_reloader=False)

else:
    if args['check_sanity']:
        pass

    if args['run']:
        DBM = DatabaseManager()

        DBM.connect_meta("PostgreSQLA", args['postgres_host'], args['postgres_port'], args['postgres_user'],
                         args['postgres_password'], args['postgres_dbname'])

        RunAPIServer(debug=args['debug'], use_reloader=args['use_reloader'])
