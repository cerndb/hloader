import json

from hloader.backend.api import app
from hloader.backend.api.v1.views import clusters, jobs
from hloader.db.DatabaseManager import DatabaseManager
from hloader.db.connectors.sqlaentities.HadoopCluster import HadoopCluster
from hloader.db.connectors.sqlaentities.Job import Job
from hloader.db.connectors.sqlaentities.OracleServer import OracleServer


class AuthConnector_Mock():

    def can_user_access_schema(self, username, database, schema):
        return True

    def get_available_objects(self, database, schema):
        return ['NOSETEST_OBJECT']

class MetaConnector_Mock():

    cluster = HadoopCluster()
    server = OracleServer()
    job = Job()

    def __init__(self):
        self.cluster.cluster_id = 1
        self.cluster.cluster_address = "nosetest_host"
        self.cluster.cluster_name = "cluster1"

        self.server.server_id = 1
        self.server.server_address = "nosetest_address"
        self.server.server_port = 1

        self.job.job_id = 1
        self.job.source_server_id = 1
        self.job.source_schema_name = "nosetest_schema"
        self.job.source_server = self.server
        self.job.destination_cluster = self.cluster
        

    def get_clusters(self, **kwargs):
        return [self.cluster]

    def get_jobs(self, **kwargs):
        return [self.job]

    def get_servers(self, **kwargs):
        return [self.server]

    def create_job(self):
        return Job()

    def add_job(self, job, _session=None):
        return 1

def test_api_v1_clusters():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = clusters.api_v1_clusters()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode())['clusters'][0].get('cluster_address') == 'nosetest_host'

def test_api_v1_get_jobs():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = jobs.api_v1_get_jobs()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode())['jobs'][0].get('source_schema_name') == 'nosetest_schema'

def test_api_v1_post_job():
    DatabaseManager.meta_connector = MetaConnector_Mock()
    DatabaseManager.auth_connector = AuthConnector_Mock()
    
    request_data = {'source_schema_name': u'schema1', 'owner_username': u'user', 'source_server_id': u'1', 'destination_path': u'path',
                   'destination_cluster_id': u'1', 'sqoop_direct': u'1', 'source_object_name': u'NOSETEST_OBJECT'}

    with app.test_request_context(method = 'POST', data = request_data):
        response = jobs.api_v1_post_job()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode()).get('job_id') == 1
