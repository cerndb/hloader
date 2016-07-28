import json

from hloader.backend.api import app
from hloader.backend.api.v1.views import clusters, jobs, logs, servers, transfers, headers, index, schemas
from hloader.db.DatabaseManager import DatabaseManager
from hloader.db.connectors.sqlaentities.HadoopCluster import HadoopCluster
from hloader.db.connectors.sqlaentities.Job import Job
from hloader.db.connectors.sqlaentities.OracleServer import OracleServer
from hloader.db.connectors.sqlaentities.Log import Log
from hloader.db.connectors.sqlaentities.Transfer import Transfer

class AuthConnector_Mock():

    def can_user_access_schema(self, username, database, schema):
        return True

    def get_available_objects(self, database, schema):
        return ['NOSETEST_OBJECT']

    def get_servers_for_user(self, username):
        return {'databases': [{'schemas': ['nosetest_schema1'], 'database': 'nosetest_server1'},
               {'schemas': ['nosetest_schema2'], 'database': 'nosetest_server2'}]}

class MetaConnector_Mock():

    cluster = HadoopCluster()
    server = OracleServer()
    job = Job()
    log = Log()
    transfer = Transfer()

    def __init__(self):
        self.cluster.cluster_id = 1
        self.cluster.cluster_address = "nosetest_host"
        self.cluster.cluster_name = "cluster1"
        self.cluster.oozie_url = "mock://test.com/"

        self.server.server_id = 1
        self.server.server_address = "nosetest_address"
        self.server.server_port = 1
        self.server.server_name = "nosetest_server1"

        self.job.job_id = 1
        self.job.source_server_id = 1
        self.job.source_schema_name = "nosetest_schema"
        self.job.source_server = self.server
        self.job.destination_cluster = self.cluster
        
        self.log.log_id = 1
        self.log.transfer_id = 1
        self.log.log_source = "nosetest_source"

        self.transfer.transfer_id = 1
        self.transfer.scheduler_transfer_id = "nosetest_id"
        self.transfer.job_id = 1

    def get_clusters(self, **kwargs):
        return [self.cluster]

    def get_jobs(self, **kwargs):
        return [self.job]

    def get_servers(self, **kwargs):
        return [self.server]

    def create_job(self):
        job = Job()
        job.job_id=1
        return job

    def add_job(self, job, _session=None):
        return 1

    def get_logs(self, _session=None, **kwargs):
        return [self.log]

    def create_log(self):
        return Log()

    def save_log(self, log, _session=None):
        return 1

    def get_transfers(self, _session=None, **kwargs):
        return [self.transfer]

    def modify_status(self, transfer_id, transfer_status, _session=None):
        return 0

    def get_source_server_for_job(self, job, _session=None):
        return self.server

    def get_destination_cluster_for_job(self, job, _session=None):
        return self.cluster

def test_api_v1_clusters():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = clusters.api_v1_clusters()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('clusters')[0].get('cluster_address') == 'nosetest_host'

def test_api_v1_get_jobs():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = jobs.api_v1_get_jobs()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('jobs')[0].get('source_schema_name') == 'nosetest_schema'

def test_api_v1_post_job():
    DatabaseManager.meta_connector = MetaConnector_Mock()
    DatabaseManager.auth_connector = AuthConnector_Mock()
    
    request_data = {'source_schema_name': u'schema1', 'owner_username': u'user', 'source_server_id': u'1', 'destination_path': u'path',
                   'destination_cluster_id': u'1', 'sqoop_direct': u'1', 'source_object_name': u'NOSETEST_OBJECT', 'workflow_suffix': u'wf'}

    with app.test_request_context(method = 'POST', data = request_data):
        response = jobs.api_v1_post_job()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('job_id') == 1

def test_api_v1_logs():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = logs.api_v1_logs()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('logs')[0].get('log_source') == 'nosetest_source'

def test_api_v1_post_log():
    DatabaseManager.meta_connector = MetaConnector_Mock()
    DatabaseManager.auth_connector = AuthConnector_Mock()
    
    request_data = {'transfer_id': u'1', 'log_source': u'nosetest_source'}

    with app.test_request_context(method = 'POST', data = request_data):
        response = logs.api_v1_post_log()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('log_id') == 1

def test_api_v1_servers():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = servers.api_v1_servers()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('servers')[0].get('server_address') == 'nosetest_address'

def test_api_v1_transfers():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = transfers.api_v1_transfers()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('transfers')[0].get('scheduler_transfer_id') == 'nosetest_id'

def test_headers():
    with app.test_request_context():
        response = headers.headers()

    assert "<b>PYTHON ENVIRONMENT VARIABLES</b>" in response

def test_api_v1():
    with app.test_request_context():
        response = index.api_v1()

    assert response=="api_v1"

def test_api_v1_schemas():
    DatabaseManager.meta_connector = MetaConnector_Mock()
    DatabaseManager.auth_connector = AuthConnector_Mock()

    request_query_string = {'owner_username': u'user'}

    with app.test_request_context(query_string = request_query_string):
        response = schemas.api_v1_schemas()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('schemas').get('available')[0].get('database') == 'nosetest_server1'
    assert json.loads(response.response[0].decode()).get('schemas').get('unavailable')[0].get('database') == 'nosetest_server2'

def test_api_v1_schemas_views():
    DatabaseManager.auth_connector = AuthConnector_Mock()

    with app.test_request_context():
        response = schemas.api_v1_schemas_views("dummy","dummy")

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('objects').get('objects')[0] == 'NOSETEST_OBJECT'
