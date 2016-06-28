import json
from flask import Response, request

from hloader.backend.api import app
from hloader.db.DatabaseManager import DatabaseManager
from werkzeug.exceptions import BadRequest

@app.route('/api/v1/logs')
def api_v1_logs():
    kwargs = {k: request.args[k] for k in
          ('log_id','transfer_id', 'log_source', 'log_path', 'log_content', 'limit', 'offset') if k in request.args}

    logs = DatabaseManager.meta_connector.get_logs(**kwargs)

    filter_key_list = [
        "log_id",
        "transfer_id",
        "log_source",
        "log_path",
        "log_content"
    ]

    result = {"logs": []}

    for log in logs:
        l = {}
        for key in filter_key_list:
            l.update({key: getattr(log, key, None)})

        result["logs"].append(l)

    return Response(json.dumps(result, indent=4), mimetype="application/json")

@app.route('/api/v1/logs', methods=['POST'])
def api_v1_post_log():
    # Check, whether we got all the required data from the user.

    required_fields = set([
        "transfer_id",
        "log_source"
    ])

    if len(set.intersection(required_fields, request.form.keys())) != len(required_fields):
        raise BadRequest("Required fields: " + ', '.join(required_fields) + ", missing fields: " + ', '.join(
            required_fields.difference(request.form.keys())))

    # insert new log
    log = DatabaseManager.meta_connector.create_log()

    log.transfer_id = request.form["transfer_id"]
    log.log_source = request.form["log_source"]

    if 'log_path' in request.form.keys():
        log.log_path = request.form["log_path"]

    if 'log_content' in request.form.keys():
        log.log_content = request.form["log_content"]

    log_id = DatabaseManager.meta_connector.save_log(log)

    result = {"log_id": log_id}

    return Response(json.dumps(result, indent=4), mimetype="application/json")
