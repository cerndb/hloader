import json

from hloader.backend.api import app
from hloader.backend.api.v1.views import clusters
from hloader.db.DatabaseManager import DatabaseManager
from hloader.db.connectors.sqlaentities.HadoopCluster import HadoopCluster



class MetaConnector_Mock():

    def get_clusters(self, **kwargs):
        cluster1 = HadoopCluster()
        cluster1.cluster_id = 1
        cluster1.cluster_address = "nosetest_host"
        cluster1.cluster_name = "cluster1"

        cluster2 = HadoopCluster()
        cluster2.cluster_id = 2
        cluster2.cluster_address = "nosetest_host"
        cluster2.cluster_name = "cluster2"

        clusterList = [cluster1, cluster2]
        return clusterList

def test_api_v1_clusters():
    DatabaseManager.meta_connector = MetaConnector_Mock()

    with app.test_request_context():
        response = clusters.api_v1_clusters()

    assert response._status == '200 OK'
    assert json.loads(response.response[0].decode())['clusters'][0].get('cluster_address') == 'nosetest_host'


