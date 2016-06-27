import json
from flask import Response, request

from hloader.backend.api import app
from hloader.db.DatabaseManager import DatabaseManager

@app.route('/api/v1/clusters')
def api_v1_clusters():
    kwargs = {k: request.args[k] for k in
          ('cluster_id', 'cluster_address', 'cluster_name', 'limit', 'offset') if k in request.args}

    clusters = DatabaseManager.meta_connector.get_clusters(**kwargs)

    filter_key_list = [
        "cluster_id",
        "cluster_address",
        "cluster_name",
    ]

    result = {
        "clusters": map(
            lambda cluster: {
                key: getattr(cluster, key, None)
                for key in filter_key_list
                },
            clusters
        )
    }

    return Response(json.dumps(dict(result), indent=4), mimetype="application/json")
