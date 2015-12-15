import sys

sys.path.insert(0, "//cern.ch/dfs/websites/t/test-hloader-server/hloader/backend/libs")

from flup.server.cgi import WSGIServer

from hloader.db.DatabaseManager import DatabaseManager
from hloader.config import config

if not (config.POSTGRE_ADDRESS and
        config.POSTGRE_PORT and
        config.POSTGRE_USERNAME and
        config.POSTGRE_PASSWORD and
        config.POSTGRE_DATABASE):
    raise Exception("Config not properly set up.")

DatabaseManager.connect_meta("PostgreSQLA",
                             config.POSTGRE_ADDRESS,
                             config.POSTGRE_PORT,
                             config.POSTGRE_USERNAME,
                             config.POSTGRE_PASSWORD,
                             config.POSTGRE_DATABASE)

DatabaseManager.connect_auth(config.AUTH_ALIAS,
                             config.AUTH_PORT,
                             config.AUTH_USERNAME,
                             config.AUTH_PASSWORD,
                             config.AUTH_SID)

from hloader.backend.api import app  # initialize the application in hloader.backend.api
from hloader.backend.api.v1 import views  # load all the views and set the api to v1 in hloader.backend.api.v1

if __name__ == "__main__":
    app.run()
    # WSGIServer(app).run()

views.__author__  # placeholder, so the views initializer script won't get deleted by accidental auto-formatting
