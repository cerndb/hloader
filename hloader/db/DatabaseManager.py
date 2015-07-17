from __future__ import absolute_import
from hloader.db.connectors.PostgreSQLAlchemyConnector import PostgreSQLAlchemyConnector
from hloader.db.IDatabaseConnector import IDatabaseConnector


class DatabaseManager(object):
    """
    Database manager class, that handles the database connection, the driver, and handles the calls for the implementations.
    :type _auth_oracle_connector: None
    :type meta_connector: IDatabaseConnector
    """

    # Central Oracle connector for authenticating and authorizing the user requests.
    _auth_oracle_connector = None

    # Connector for the PostgreSQL/MongoDB database containing for example the job and transfer entries.
    meta_connector = None
    """:type : IDatabaseConnector"""

    @staticmethod
    def connect_oracle(address, port, username, password, database):
        # DatabaseManager._auth_oracle_connector = ...
        pass

    @staticmethod
    def connect_meta(type, address, port, username, password, database):
        DatabaseManager.meta_connector = {
            "PostgreSQLA": PostgreSQLAlchemyConnector(address, port, username, password, database)
        }.get(type, None)

    @staticmethod
    def get_servers():
        return DatabaseManager.meta_connector.get_servers()
