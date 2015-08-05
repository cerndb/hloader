import json

from flask import Response, request

from hloader.backend.api import app
from hloader.backend.api.v1.util.get_username import get_username
from hloader.db.DatabaseManager import DatabaseManager

__author__ = 'dstein'


@app.route('/api/v1/schemas')
def api_v1_schemas():
    # TODO
    # auth = DatabaseManager.auth_connector.get_servers_for_user(get_username(request.remote_user))
    auth = DatabaseManager.auth_connector.get_servers_for_user(get_username("CERN\kdziedzi"))
    meta = DatabaseManager.meta_connector.get_servers()

    meta_aliases = map(lambda server: server.server_name, meta)

    available = filter(lambda key: key if key["database"] in meta_aliases else None, auth["databases"])
    unavailable = filter(lambda key: key if key["database"] not in meta_aliases else None, auth["databases"])

    result = {
        "schemas": {
            "available": available,
            "unavailable": unavailable
        }
    }

    return Response(json.dumps(result, indent=4), mimetype="application/json")
