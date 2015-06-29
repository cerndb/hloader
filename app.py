from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Perform a shell export for HLOADER_CONFIG to indicate the type of
# configuration. See config.py for details about each configuration.
# Available options are:
#   * config.ProductionConfig (default)
#   * config.DevelopmentConfig
#
# Example: export HLOADER_CONFIG="config.DevelopmentConfig"

hloader_config = os.environ.get('HLOADER_CONFIG')
if hloader_config is not None:
    app.config.from_object(hloader_config)
else:
    print "HLOADER_CONFIG environment variable not set. Using \
          'config.ProductionConfig' as default"
    app.config.from_object(config.ProductionConfig)

db = SQLAlchemy(app)


@app.route('/api/v1')
def api_v1_index():
    return "This is the landing page for the HLoader REST API v1"


if __name__ == '__main__':
    app.run()
