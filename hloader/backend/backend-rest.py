# from os import environ
#
# from hloader.db.DatabaseManager import DatabaseManager
#
# USERNAME = "user"
#
# __author__ = 'dstein'
#
#
# # Initialize database connection
# postgre_address = environ.get('POSTGRE_ADDRESS')
# postgre_port = environ.get('POSTGRE_PORT')
# postgre_username = environ.get('POSTGRE_USERNAME')
# postgre_password = environ.get('POSTGRE_PASSWORD')
# postgre_database = environ.get('POSTGRE_DATABASE')
#
# if not (postgre_address and postgre_port and postgre_username and postgre_password and postgre_database):
#     raise Exception("Environmental variables are not properly set up.")
#
# DatabaseManager.connect_meta("PostgreSQLA",
#                              postgre_address, postgre_port, postgre_username, postgre_password, postgre_database)
#

from __future__ import absolute_import

import sys

sys.path.insert(0, "libs")
from flup.server.fcgi import WSGIServer

from hloader.backend.api import app
from hloader.backend.api.v1 import views

if __name__ == "__main__":
    WSGIServer(app).run()

views.__author__
