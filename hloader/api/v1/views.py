from hloader.api.v1 import app
from hloader.db.DatabaseManager import DatabaseManager

from __future__ import absolute_import
from flask import Response, json, redirect, request
from sqlalchemy.orm import class_mapper


@app.route('/api')
def api_index():
    """
     This route must be redirected to a suitable version of the HLoader API
     In future the API may well be extended/changed, and backward
     compatibility will guarantee that things don't break.

    :return: Redirect to HLoader API v1
    """
    return redirect('/api/v1', code=302)


@app.route('/api/v1')
def api_index_default():
    """
    Returns to index page
    :return: Returns to index page
    """
    return "This is the landing page for the HLoader REST API v1"


@app.route('/api/v1/HL_SERVERS')
def api_hl_servers():
    if set(request.args) <= {'server_id', 'server_address', 'server_port', 'server_name', 'limit', 'offset'}:
        s_id = request.args.get('server_id')
        address = request.args.get('server_address')
        port = request.args.get('server_port')
        name = request.args.get('server_name')
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', 0)

        serialized_dict = [
            serialize(server)
            for server in DatabaseManager.meta_connector.get_servers(server_id=s_id,
                                                                     server_address=address,
                                                                     server_port=port,
                                                                     server_name=name,
                                                                     limit=limit,
                                                                     offset=offset)
            ]
        return Response(json.dumps(serialized_dict,
                                   indent=4),
                        mimetype="application/json")

    else:
        raise Exception("InvalidRequestError.")


@app.route('/api/v1/HL_CLUSTERS')
def api_hl_clusters():
    if set(request.args) <= {'cluster_id', 'cluster_address', 'cluster_name', 'limit', 'offset'}:
        c_id = request.args.get('cluster_id')
        address = request.args.get('cluster_address')
        name = request.args.get('cluster_name')
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', 0)

        serialized_dict = [
            serialize(cluster)
            for cluster in DatabaseManager.meta_connector.get_clusters(cluster_id=c_id,
                                                                       cluster_address=address,
                                                                       cluster_name=name,
                                                                       limit=limit,
                                                                       offset=offset)
            ]
        return Response(json.dumps(serialized_dict,
                                   indent=4),
                        mimetype="application/json")
    else:
        raise Exception("InvalidRequestError.")


@app.route('/api/v1/HL_TRANSFERS')
def api_hl_transfers():
    if set(request.args) <= {'transfer_id', 'scheduler_transfer_id', 'job_id', 'transfer_status', 'limit', 'offset'}:
        t_id = request.args.get('transfer_id')
        st_id = request.args.get('scheduler_transfer_id')
        j_id = request.args.get('job_id')
        status = request.args.get('transfer_status')
        limit = request.args.get('limit', None)
        offset = request.args.get('offset', 0)

        serialized_dict = [
            serialize(cluster)
            for cluster in DatabaseManager.meta_connector.get_transfers(transfer_id=t_id,
                                                                        scheduler_transfer_id=st_id,
                                                                        job_id=j_id,
                                                                        transfer_status=status,
                                                                        limit=limit,
                                                                        offset=offset)
            ]
        return Response(json.dumps(serialized_dict,
                                   indent=4),
                        mimetype="application/json")
    else:
        raise Exception("InvalidRequestError.")


def serialize(model):
    """
    Transforms a model into a dictionary which can be dumped to JSON.
    """
    columns = [c.key for c in class_mapper(model.__class__).columns]
    return dict((c, getattr(model, c)) for c in columns)
