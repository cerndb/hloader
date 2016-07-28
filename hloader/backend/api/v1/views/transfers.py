import json
from flask import Response, request

from hloader.backend.api import app
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
