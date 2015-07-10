from hloader.db.connectors.PostgreSQLAlchemyConnector import PostgreSQLAlchemyConnector


class DatabaseManager:
    """
    Database manager class, that handles the database connection, the driver, and handles the calls for the implementations.
    """

    # Central Oracle connector for authenticating and authorizing the user requests.
    _auth_oracle_connector = None

    # Connector for the PostgreSQL/MongoDB database containing for example the job and transfer entries.
    _meta_connector = None

    @staticmethod
    def connect_oracle(address, port, username, password, database):
        # DatabaseManager._auth_oracle_connector = ...
        pass

    @staticmethod
    def connect_meta(type, address, port, username, password, database):
        DatabaseManager._meta_connector = {
            "PostgreSQLA": PostgreSQLAlchemyConnector(address, port, username, password, database)
        }.get(type, None)

    # ------------------------------------------------------------------------------------------------------------------

