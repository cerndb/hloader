import json
from flask import Response, request

from hloader.backend.api import app
from hloader.db.DatabaseManager import DatabaseManager

@app.route('/api/v1/clusters')
def api_v1_clusters():
    kwargs = {k: request.args[k] for k in
          ('cluster_id', 'cluster_address', 'cluster_name', 'oozie_url', 'limit', 'offset') if k in request.args}

    clusters = DatabaseManager.meta_connector.get_clusters(**kwargs)

    filter_key_list = [
        "cluster_id",
        "cluster_address",
        "cluster_name",
        "oozie_url"
    ]


    result = {"clusters": []}

    for cluster in clusters:
        c = {}
        for key in filter_key_list:
            c.update({key: getattr(cluster, key, None)})

        result["clusters"].append(c)

    return Response(json.dumps(result, indent=4), mimetype="application/json")
