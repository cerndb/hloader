



class Job(object):
    job_id = None

    source_server_id = None
    source_schema_name = None
    source_object_name = None

    destination_cluster_id = None
    destination_path = None

    owner_username = None
    coordinator_suffix = None
    workflow_suffix = None

    oozie_job_id = None

    sqoop_nmap = None
    sqoop_splitting_column = None
    sqoop_incremental_method = None
    sqoop_direct = None

    start_time = None
    end_time = None
    interval = None

    def get_source_server(self):
        """

        """
        raise Exception("Not implemented.")

    def get_destination_cluster(self):
        """

        """
        raise Exception("Not implemented.")
