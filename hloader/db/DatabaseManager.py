from hloader.db.connectors.PostgreSQLConnector import PostgreSQLConnector

__author__ = 'dstein'


class DatabaseManager:
    """
    Database manager class, that handles the database connection, the driver, and handles the calls for the implementations.
    """

    _connector = None

    def __init__(self, connection_string=""):
        super().__init__(self)
        _connector = PostgreSQLConnector(connection_string)

    @staticmethod
    def get_servers():
        return DatabaseManager._connector.get_servers()

    @staticmethod
    def get_clusters():
        return DatabaseManager._connector.get_clusters()

    @staticmethod
    def get_jobs(database="*"):
        return DatabaseManager._connector.get_jobs(database=database)

    @staticmethod
    def get_ready_jobs():
        return DatabaseManager._connector.get_ready_jobs()

    @staticmethod
    def get_transfers(job="*", state="*", limit="10"):
        return DatabaseManager._connector.get_transfers(job=job, state=state, limit=limit)
