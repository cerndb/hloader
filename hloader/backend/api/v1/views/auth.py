import json

from flask import Response, request

from hloader.backend.api import app
from hloader.db.DatabaseManager import DatabaseManager

__author__ = 'dstein'


@app.route('/api/v1/auth')
def api_v1_auth():
    auth = DatabaseManager.auth_connector.get_servers_for_user(request.remote_user)
    return Response(json.dumps(auth, indent=4), mimetype="application/json")
