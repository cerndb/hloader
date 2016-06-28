import json
from flask import Response, request

from hloader.backend.api import app
from werkzeug.exceptions import BadRequest
from hloader.db.DatabaseManager import DatabaseManager
from hloader.backend.api.v1.util.json_datetime_handler_default import json_datetime_handler_default

@app.route('/api/v1/transfers')
def api_v1_transfers():
    kwargs = {k: request.args[k] for k in
          ('transfer_id', 'scheduler_transfer_id', 'job_id', 'transfer_status', 'transfer_start', 'transfer_last_update', 'last_modified_value', 'limit', 'offset') if k in request.args}

    transfers = DatabaseManager.meta_connector.get_transfers(**kwargs)

    filter_key_list = [
        "transfer_id",
        "scheduler_transfer_id",
        "job_id",
        "transfer_status",
        "transfer_start", # %2B is escape literal for + symbol in the url
        "transfer_last_update",
        "last_modified_value"
    ]

    result = {"transfers": []}

    for transfer in transfers:
        t = {}
        for key in filter_key_list:
            t.update({key: getattr(transfer, key, None)})

        result["transfers"].append(t)

    return Response(json.dumps(result, indent=4, default=json_datetime_handler_default), mimetype="application/json")

@app.route('/api/v1/transfers', methods=['POST'])
def api_v1_post_transfer():
    # Check, whether we got all the required data from the user.

    required_fields = set([
        "job_id",
        "last_modified_value"
    ])

    request_form_keys=request.form.keys()

    if len(set.intersection(required_fields, request_form_keys)) != len(required_fields):
        raise BadRequest("Required fields: " + ', '.join(required_fields) + ", missing fields: " + ', '.join(
            required_fields.difference(request_form_keys)))

    # insert new log
    transfer = DatabaseManager.meta_connector.create_transfer()

    transfer.job_id = request.form["job_id"]
    transfer.last_modified_value = request.form["last_modified_value"]

    if 'scheduler_transfer_id' in request_form_keys:
        transfer.scheduler_transfer_id = request.form["scheduler_transfer_id"]

    if 'transfer_status' in request_form_keys:
        transfer.transfer_status = request.form["transfer_status"]

    if 'transfer_start' in request_form_keys:
        transfer.transfer_start = request.form["transfer_start"]

    if 'transfer_last_update' in request_form_keys:
        transfer.transfer_last_update = request.form["transfer_last_update"]

    transfer_id = DatabaseManager.meta_connector.add_transfer(transfer)

    result = {"transfer_id": transfer_id}

    return Response(json.dumps(result, indent=4), mimetype="application/json")

@app.route('/api/v1/transfers', methods=['PUT'])
def api_v1_put_transfer():
    # Check, whether we got all the required data from the user.

    required_fields = set([
        "transfer_id",
        "transfer_status"
    ])

    request_form_keys=request.form.keys()

    if len(set.intersection(required_fields, request_form_keys)) != len(required_fields):
        raise BadRequest("Required fields: " + ', '.join(required_fields) + ", missing fields: " + ', '.join(
            required_fields.difference(request_form_keys)))

    status_update = DatabaseManager.meta_connector.modify_status(request.form["transfer_id"],request.form["transfer_status"])
    result = {"status_update": status_update}

    return Response(json.dumps(result, indent=4), mimetype="application/json")
