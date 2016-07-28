import json
import re
from flask import Response, request
from werkzeug.exceptions import abort, BadRequest

from hloader.backend.api import app
from hloader.backend.api.v1.util.get_username import get_username
from hloader.backend.api.v1.util.json_datetime_handler_default import json_datetime_handler_default
from hloader.db.DatabaseManager import DatabaseManager
from hloader.transfer.runners.OozieRunner import OozieRunner

@app.route('/api/v1/jobs', methods=['GET'])
def api_v1_get_jobs():
    kwargs = {k: request.args[k] for k in
          ('job_id', 'source_server_id', 'source_schema_name', 'source_object_name', 'destination_cluster_id', 
          'destination_path', 'owner_username', 'coordinator_suffix', 'workflow_suffix', 'oozie_job_id', 'sqoop_nmap', 'sqoop_splitting_column', 'sqoop_incremental_method',
          'sqoop_direct', 'start_time', 'end_time', 'interval', 'job_last_update', 'limit', 'offset') if k in request.args}

    jobs = DatabaseManager.meta_connector.get_jobs(**kwargs)

    filter_key_list = [
        "job_id",
        "source_server_id",
        "source_schema_name",
        "source_object_name",
        "destination_cluster_id",
        "destination_path",
        "owner_username",
        "coordinator_suffix",
        "workflow_suffix",
        "oozie_job_id",
        "sqoop_nmap",
        "sqoop_splitting_column",
        "sqoop_incremental_method",
        "sqoop_direct",
        "start_time",
        "end_time",
        "interval",
        "job_last_update",
        "source_server_alias",
        "destination_cluster_alias"
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
        "owner_username",
        "workflow_suffix",
        "sqoop_direct"
    ])

    request_form_keys=request.form.keys()

    if len(set.intersection(required_fields, request_form_keys)) != len(required_fields):
        raise BadRequest("Required fields: " + ', '.join(required_fields) + ", missing fields: " + ', '.join(
            required_fields.difference(request_form_keys)))

    # Check, whether the user could access the schema.
    source_server_id_ = int(request.form["source_server_id"])
    server = DatabaseManager.meta_connector.get_servers(**{"server_id": source_server_id_})
    if len(server) < 1:
        raise BadRequest("Server with ID " + source_server_id_ + " not found.")
    server = server[0]

    source_schema_name_ = request.form["source_schema_name"]
    owner_username = request.form["owner_username"]

    # TODO
    # if not DatabaseManager.auth_connector.can_user_access_schema(get_username(request.remote_user), database, schema):
    if not DatabaseManager.auth_connector.can_user_access_schema(get_username("CERN\\"+owner_username), server.server_name,
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
    job.owner_username = get_username("CERN\\"+owner_username)

    job.workflow_suffix = request.form["workflow_suffix"]

    if 'coordinator_suffix' in request_form_keys:
        job.coordinator_suffix = request.form["coordinator_suffix"]

    if 'sqoop_nmap' in request_form_keys:
        job.sqoop_nmap = request.form["sqoop_nmap"]

    if 'sqoop_splitting_column' in request_form_keys:
        job.sqoop_splitting_column = request.form["sqoop_splitting_column"]

    if 'sqoop_incremental_method' in request_form_keys:
        job.sqoop_incremental_method = request.form["sqoop_incremental_method"]
    
    job.sqoop_direct = request.form["sqoop_direct"]

    if 'start_time' in request_form_keys:
        job.start_time = request.form["start_time"]

    if 'end_time' in request_form_keys:
        job.end_time = request.form["end_time"]

    if 'interval' in request_form_keys:
        job.interval = request.form["interval"]

    if 'job_last_update' in request_form_keys:
        job.job_last_update = request.form["job_last_update"]

    runner = OozieRunner()
    job.oozie_job_id=runner.submit(job)

    DatabaseManager.meta_connector.add_job(job)

    result = None

    if job.coordinator_suffix is None:
        status_code = runner.manage(job,'start')
        result = {"job_id": job.job_id, "oozie_job_id": job.oozie_job_id, "start status_code": status_code}

    else:
        result = {"job_id": job.job_id, "oozie_job_id": job.oozie_job_id}

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")

@app.route('/api/v1/jobs', methods=['DELETE'])
def api_v1_delete_job():
    # Check, whether we got all the required data from the user.
    required_fields = set([
        "job_id"
    ])

    request_form_keys=request.form.keys()

    if len(set.intersection(required_fields, request_form_keys)) != len(required_fields):
        raise BadRequest("Required fields: " + ', '.join(required_fields) + ", missing fields: " + ', '.join(
            required_fields.difference(request_form_keys)))

    #get oozie_job_id for the job
    jobs = DatabaseManager.meta_connector.get_jobs(**{"job_id": request.form["job_id"]})
    
    result = None    

    if len(jobs)>0:
        job=jobs[0]

        runner = OozieRunner()
        status_code = runner.manage(job,'kill')

        DatabaseManager.meta_connector.delete_job(job)
    
        result = {"job_id": job.job_id, "oozie_job_id": job.oozie_job_id, "kill status_code": status_code}

    else:
        result = {"message": "job does not exist"}

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")
    
