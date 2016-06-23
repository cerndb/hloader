from flask import Flask
from flask.ext.cors import CORS

app = Flask(__name__)

from v1.views import clusters, headers, index, jobs, schemas, servers, transfers, logs

#CORS(app, resources=r"/api/*", allowed_headers="Content-Type")
