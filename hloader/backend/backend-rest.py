from __future__ import absolute_import

import sys

sys.path.insert(0, "//cern.ch/dfs/websites/t/test-hloader-server/hloader/backend/libs")

from flup.server.cgi import WSGIServer

from hloader.db.DatabaseManager import DatabaseManager
from hloader.config import AUTH_ALIAS, AUTH_PORT, AUTH_USERNAME, AUTH_PASSWORD, AUTH_SID
from hloader.config import POSTGRE_ADDRESS, POSTGRE_DATABASE, POSTGRE_PASSWORD, POSTGRE_PORT, POSTGRE_USERNAME

if not (POSTGRE_ADDRESS and POSTGRE_PORT and POSTGRE_USERNAME and POSTGRE_PASSWORD and POSTGRE_DATABASE):
    raise Exception("Config not properly set up.")

DatabaseManager.connect_meta("PostgreSQLA",
                             POSTGRE_ADDRESS, POSTGRE_PORT, POSTGRE_USERNAME, POSTGRE_PASSWORD, POSTGRE_DATABASE)

DatabaseManager.connect_auth(AUTH_ALIAS, AUTH_PORT, AUTH_USERNAME, AUTH_PASSWORD, AUTH_SID)

from hloader.backend.api import app  # initialize the application in hloader.backend.api
from hloader.backend.api.v1 import views  # load all the views and set the api to v1 in hloader.backend.api.v1

if __name__ == "__main__":
    app.run()
    # WSGIServer(app).run()

views.__author__  # placeholder, so the views initializer script won't get deleted by accidental auto-formatting
