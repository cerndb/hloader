import json
import re
from flask import Response, request
from werkzeug.exceptions import abort, BadRequest

from hloader.backend.api import app
from hloader.backend.api.v1.util.get_username import get_username
from hloader.backend.api.v1.util.json_datetime_handler_default import json_datetime_handler_default
from hloader.db.DatabaseManager import DatabaseManager




@app.route('/api/v1/jobs', methods=['GET'])
def api_v1_get_jobs():
    # TODO if the user is an administrator for the system, allow them to see every job
    # kwargs = {"owner_username": get_username(request.remote_user)}
    kwargs = {"owner_username": get_username(r"CERN\kdziedzi")}

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

    result = {"jobs": []}

    for job in jobs:
        j = {}
        for key in filter_key_list:
            j.update({key: getattr(job, key, None)})

        j.update({"source_server_alias": job.source_server.server_name})
        j.update({"destination_cluster_alias": job.destination_cluster.cluster_name})

        result["jobs"].append(j)

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")


@app.route('/api/v1/jobs', methods=['POST'])
def api_v1_post_job():
    """
    Add a new job to the database. If the user is allowed to access the given schema, put it in as a new job.
    :return: the inserted job
    """

    # Check, whether we got all the required data from the user.
    required_fields = set([
        "source_server_id",
        "source_schema_name",
        "source_object_name",
        "destination_cluster_id",
        "destination_path",
        "start_time",
        "interval",
    ])
    if len(set.intersection(required_fields, request.form.keys())) != len(required_fields):
        raise BadRequest("Required fields: " + ', '.join(required_fields) + ", missing fields: " + ', '.join(
            required_fields.difference(request.form.keys())))

    # Check, whether the user could access the schema.
    source_server_id_ = int(request.form["source_server_id"])
    server = DatabaseManager.meta_connector.get_servers(**{"server_id": source_server_id_})
    if len(server) < 1:
        raise BadRequest("Server with ID " + source_server_id_ + " not found.")
    server = server[0]

    source_schema_name_ = request.form["source_schema_name"]

    # TODO
    # if not DatabaseManager.auth_connector.can_user_access_schema(get_username(request.remote_user), database, schema):
    if not DatabaseManager.auth_connector.can_user_access_schema(get_username(r"CERN\kdziedzi"), server.server_name,
                                                                 source_schema_name_):
        abort(403)

    # Check, whether the selected schema has the provided object
    source_object_name_ = request.form["source_object_name"]
    if source_object_name_.upper() not in (
            obj.upper() for obj
            in DatabaseManager.auth_connector.get_available_objects(server.server_name, source_schema_name_)
    ):
        raise BadRequest("Object with name " + source_object_name_ + " not found.")

    # cluster exists
    destination_cluster_id_ = int(request.form["destination_cluster_id"])
    cluster = DatabaseManager.meta_connector.get_clusters(**{"cluster_id": destination_cluster_id_})
    if len(cluster) < 1:
        raise BadRequest("Cluster with ID " + destination_cluster_id_ + " not found.")
    cluster = cluster[0]

    # destination path valid
    destination_path_ = request.form["destination_path"]
    if re.match("^[a-zA-Z0-9-_/]*$", destination_path_) is None:
        raise BadRequest("The relative path is not valid. Please only use the a-z, A-Z, 0-9, -, _, / characters.")

    # TODO check start time
    # TODO check interval

    # insert new job
    job = DatabaseManager.meta_connector.create_job()

    job.source_server_id = source_server_id_
    job.source_schema_name = source_schema_name_
    job.source_object_name = source_object_name_

    job.destination_cluster_id = destination_cluster_id_
    job.destination_path = destination_path_

    # TODO
    # job.owner_username = get_username(request.remote_user)
    job.owner_username = get_username(r"CERN\kdziedzi")

    job.sqoop_direct = True

    # TODO set start time and interval

    job_id = DatabaseManager.meta_connector.add_job(job)

    result = {"job_id": job_id}

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")
