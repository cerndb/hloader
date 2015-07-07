from flask import Flask, Response, json, redirect
import os
import sys
import argparse

from db.DatabaseManager import DatabaseManager

app = Flask(__name__)

@app.route('/api')
def api_index():
    # This route must be redirected to a suitable version of the HLoader API
    # In future the API may well be extended/changed, and backward
    # compatibility will guarantee that things don't break.

    # Redirect to HLoader API v1
    return redirect('/api/v1', code=302)

@app.route('/api/v1')
def api_v1_index():
    return "This is the landing page for the HLoader REST API v1"

@app.route('/api/v1/hl_servers')
def api_v1_hl_servers():
    return Response(json.dumps(connector.get_servers(), indent=4), mimetype='application/json')


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
parser.add_argument('--postgres-dbname', action='store', help='Specify PostgreSQL database name', default='hloader-db')
parser.add_argument('--postgres-user', action='store', help='Specify PostgreSQL username', default='hluser')
parser.add_argument('--postgres-password', action='store', help='Specify PostgreSQL password')

args = vars(parser.parse_args())


if len(sys.argv) == 1:
    parser.print_help()

if args['check_sanity'] == True:
    pass

if args['run'] == True:
    connector = DatabaseManager(args['postgres_host'], args['postgres_dbname'], args['postgres_user'], args['postgres_password'])
    app.run(debug=args['debug'], use_reloader=args['use_reloader'])
