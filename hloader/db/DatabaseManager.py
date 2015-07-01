from db.connectors.PostgreSQLConnector import PostgreSQLConnector

class DatabaseManager:
    """
    Database manager class, that handles the database connection, the driver, and handles the calls for the implementations.
    """

    _connector = None

    def __init__(self, host, dbname, user, password):
        _connector = PostgreSQLConnector(host, dbname, user, password)

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
