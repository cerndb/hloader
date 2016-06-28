import json
from flask import request, Response

from hloader.backend.api import app
from hloader.db.DatabaseManager import DatabaseManager




@app.route('/api/v1/servers')
def api_v1_servers():
    """

    :return: Server list
    """
    kwargs = {k: request.args[k] for k in
              ('server_id', 'server_address', 'server_port', 'server_name', 'limit', 'offset') if k in request.args}

    servers = DatabaseManager.meta_connector.get_servers(**kwargs)
    
    filter_key_list = [
        "server_id",
        "server_address",
        "server_port",
        "server_name" 
    ]

    result = {"servers": []}

    for server in servers:
        s = {}
        for key in filter_key_list:
            s.update({key: getattr(server, key, None)})

        result["servers"].append(s)

    return Response(json.dumps(result, indent=4), mimetype="application/json")
