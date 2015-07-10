from hloader.entities.HadoopCluster import HadoopCluster
from hloader.entities.OracleServer import OracleServer

__author__ = 'dstein'


class Job(object):
    job_id = None
    source_server_id = None
    source_database_name = None
    source_table_name = None
    destination_cluster_id = None
    destination_path = None
    query_columns = None
    query_source = None
    query_conditions = None
    sqoop_nmap = None
    sqoop_splitting_column = None
    sqoop_incremental_method = None
    sqoop_direct = None
    start_time = None
    interval = None

    def get_source_server(self) -> OracleServer:
        raise Exception("Not implemented.")

    def get_destination_cluster(self) -> HadoopCluster:
        raise Exception("Not implemented.")
