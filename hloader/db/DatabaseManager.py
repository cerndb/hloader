from hloader.db.connectors.OracleAuthConnector import OracleAuthConnector
from hloader.db.connectors.PostgreSQLAlchemyConnector import PostgreSQLAlchemyConnector
from hloader.db import IDatabaseConnector


class DatabaseManager(object):
    """
    Database manager class, that handles the database connection, the driver, and handles the calls for the implementations.
    :type _auth_oracle_connector: None
    :type meta_connector: IDatabaseConnector
    """

    # Central Oracle connector for authenticating and authorizing the user requests.
    auth_connector = None

    # Connector for the PostgreSQL/MongoDB database containing for example the job and transfer entries.
    meta_connector = None
    """:type : IDatabaseConnector"""

    @staticmethod
    def connect_auth(address, port, username, password, database):
        DatabaseManager.auth_connector = OracleAuthConnector(address, port, username, password, database)

    @staticmethod
    def connect_meta(type, address, port, username, password, database):
        DatabaseManager.meta_connector = {
            "PostgreSQLA": PostgreSQLAlchemyConnector(address, port, username, password, database)
        }.get(type, None)
