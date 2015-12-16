import json
from flask import Response

from hloader.backend.api import app
from hloader.backend.api.v1.util.json_datetime_handler_default import json_datetime_handler_default
from hloader.db.DatabaseManager import DatabaseManager




@app.route('/api/v1/clusters')
def api_v1_clusters():
    clusters = DatabaseManager.meta_connector.get_clusters()

    filter_key_list = [
        "cluster_id",
        # "cluster_address",
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

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")
