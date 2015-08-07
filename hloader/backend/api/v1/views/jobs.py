import json

from flask import Response

from hloader.backend.api import app
from hloader.backend.api.v1.util.json_datetime_handler_default import json_datetime_handler_default
from hloader.backend.api.v1.util.get_username import get_username
from hloader.db.DatabaseManager import DatabaseManager

__author__ = 'dstein'


@app.route('/api/v1/jobs', methods=['GET'])
def api_v1_get_jobs():
    # TODO if the user is an administrator for the system, allow them to see every job
    # kwargs = {"owner_username": get_username(request.remote_user)}
    kwargs = {"owner_username": get_username("CERN\kdziedzi")}

    jobs = DatabaseManager.meta_connector.get_jobs(**kwargs)

    filter_key_list = [
        "job_id",
        "source_server_id",
        "source_schema_name",
        "source_object_name",
        "destination_cluster_id",
        "destination_path",
        "owner_username",
        "sqoop_nmap",
        "sqoop_splitting_column",
        "sqoop_incremental_method",
        "sqoop_direct",
        "start_time",
        "interval",
    ]

    result = {
        "jobs": map(
            lambda job: {
                key: getattr(job, key, None)
                for key in filter_key_list
                },
            jobs
        )
    }

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")
