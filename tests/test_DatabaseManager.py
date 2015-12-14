from __future__ import absolute_import
from hloader.db.DatabaseManager import DatabaseManager
from hloader.db.connectors.PostgreSQLAlchemyConnector import PostgreSQLAlchemyConnector

from sqlalchemy.orm import Session, scoped_session

from ConfigParser import SafeConfigParser
parser = SafeConfigParser()
parser.read("config.ini")

class TestPostgreSQLAlchemyConnector:
    def test_setup_database(self):

        DatabaseManager.connect_meta("PostgreSQLA",
                                     parser.get('default', 'POSTGRE_ADDRESS'),
                                     parser.get('default', 'POSTGRE_PORT'),
                                     parser.get('default', 'POSTGRE_USERNAME'),
                                     parser.get('default', 'POSTGRE_PASSWORD'),
                                     parser.get("default", "POSTGRE_DATABASE")
                                     )
        DatabaseManager.meta_connector.setup_database()
        assert isinstance(DatabaseManager.meta_connector, PostgreSQLAlchemyConnector)


    def test_create_session(self):
        session_registry = DatabaseManager.meta_connector.create_session()
        assert isinstance(session_registry, scoped_session)

        session = session_registry()
        assert isinstance(session, Session)

        session_registry.remove()
