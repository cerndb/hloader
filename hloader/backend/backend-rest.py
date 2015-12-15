import sys

sys.path.insert(0, "//cern.ch/dfs/websites/t/test-hloader-server/hloader/backend/libs")

from flup.server.cgi import WSGIServer

from hloader.db.DatabaseManager import DatabaseManager
from hloader.config import Config

if not (Config.POSTGRE_ADDRESS and
        Config.POSTGRE_PORT and
        Config.POSTGRE_USERNAME and
        Config.POSTGRE_PASSWORD and
        Config.POSTGRE_DATABASE):
    raise Exception("Config not properly set up.")

DatabaseManager.connect_meta("PostgreSQLA",
                             Config.POSTGRE_ADDRESS,
                             Config.POSTGRE_PORT,
                             Config.POSTGRE_USERNAME,
                             Config.POSTGRE_PASSWORD,
                             Config.POSTGRE_DATABASE)

DatabaseManager.connect_auth(Config.AUTH_ALIAS,
                             Config.AUTH_PORT,
                             Config.AUTH_USERNAME,
                             Config.AUTH_PASSWORD,
                             Config.AUTH_SID)

from hloader.backend.api import app  # initialize the application in hloader.backend.api
from hloader.backend.api.v1 import views  # load all the views and set the api to v1 in hloader.backend.api.v1

if __name__ == "__main__":
    app.run()
    # WSGIServer(app).run()

views.__author__  # placeholder, so the views initializer script won't get deleted by accidental auto-formatting
