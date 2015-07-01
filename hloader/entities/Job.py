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
    update_difference = None

    def get_source_server(self) -> OracleServer:
        """
        The DB connector should handle getting the connected Oracle Server entity.
        :return: the connected Oracle Server entity
        :rtype: OracleServer
        """

        # TODO temporary solution
        # raise Exception("Not implemented.")
        server = OracleServer()
        server.server_id = 1
        server.server_address = "d3r-s.cern.ch"
        server.server_port = 10121
        server.server_name = "d3r.cern.ch"

        return server
