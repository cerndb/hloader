import json
from flask import Response, request

from hloader.backend.api import app
from hloader.backend.api.v1.util.get_username import get_username
from hloader.db.DatabaseManager import DatabaseManager

@app.route('/api/v1/schemas')
def api_v1_schemas():
    # TODO
    # auth = DatabaseManager.auth_connector.get_servers_for_user(get_username(request.remote_user))

    """
    :return: Schemas in the DB
    """

    owner_username=request.args["owner_username"]
    if owner_username is None:
        raise BadRequest("Indicate the owner_username parameter")

    auth = DatabaseManager.auth_connector.get_servers_for_user(get_username("CERN\\"+owner_username))
    meta = DatabaseManager.meta_connector.get_servers()
    print(auth)
    meta_aliases = list(map(lambda server: server.server_name, meta))
    print(meta_aliases)
    available = list(filter(lambda key: key if key["database"] in meta_aliases else None, auth["databases"]))
    unavailable = list(filter(lambda key: key if key["database"] not in meta_aliases else None, auth["databases"]))
    print(available)
    print(unavailable)
    result = {
        "schemas": {
            "available": available,
            "unavailable": unavailable
        }
    }
    print(result)
    return Response(json.dumps(result, indent=4), mimetype="application/json")

@app.route('/api/v1/schemas/<database>/<schema>')
def api_v1_schemas_views(database, schema):
    # TODO
    # if not DatabaseManager.auth_connector.can_user_access_schema(get_username(request.remote_user), database, schema):
    # if not DatabaseManager.auth_connector.can_user_access_schema(get_username("CERN\kdziedzi"), database, schema):
    #     abort(403)

    """

    :param database:
    :param schema:
    :return: Views in the schema
    """
    objects = DatabaseManager.auth_connector.get_available_objects(database, schema)

    result = {
        "objects": {
            "database": database,
            "schema": schema,
            "objects": objects
        }
    }

    return Response(json.dumps(result, indent=4), mimetype="application/json")
