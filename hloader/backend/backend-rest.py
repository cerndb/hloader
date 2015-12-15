import sys

sys.path.insert(0, "//cern.ch/dfs/websites/t/test-hloader-server/hloader/backend/libs")

from flup.server.cgi import WSGIServer

from hloader.db.DatabaseManager import DatabaseManager
from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read("config.ini")

if not (parser.get('default', 'POSTGRE_ADDRESS') and
        parser.get('default', 'POSTGRE_PORT') and
        parser.get('default', 'POSTGRE_USERNAME') and
        parser.get('default', 'POSTGRE_PASSWORD') and
        parser.get('default', 'POSTGRE_DATABASE')):
    raise Exception("Config not properly set up.")

DatabaseManager.connect_meta("PostgreSQLA",
                             parser.get('default', 'POSTGRE_ADDRESS'),
                             parser.get('default', 'POSTGRE_PORT'),
                             parser.get('default', 'POSTGRE_USERNAME'),
                             parser.get('default', 'POSTGRE_PASSWORD'),
                             parser.get('default', 'POSTGRE_DATABASE'))

DatabaseManager.connect_auth(parser.get('default', 'AUTH_ALIAS'),
                             parser.get('default', 'AUTH_PORT'),
                             parser.get('default', 'AUTH_USERNAME'),
                             parser.get('default', 'AUTH_PASSWORD'),
                             parser.get('default', 'AUTH_SID'))

from hloader.backend.api import app  # initialize the application in hloader.backend.api
from hloader.backend.api.v1 import views  # load all the views and set the api to v1 in hloader.backend.api.v1

if __name__ == "__main__":
    app.run()
    # WSGIServer(app).run()

views.__author__  # placeholder, so the views initializer script won't get deleted by accidental auto-formatting
