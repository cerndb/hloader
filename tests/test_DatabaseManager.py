from hloader.db import DatabaseManager
from hloader.db.connectors import PostgreSQLAlchemyConnector

from sqlalchemy.orm import Session, scoped_session

from hloader.config import Config

class TestPostgreSQLAlchemyConnector:
    '''
    def test_setup_database(self):

        DatabaseManager.connect_meta("PostgreSQLA",
                                     Config.AUTH_TABLE,
                                     Config.POSTGRE_PORT,
                                     Config.POSTGRE_USERNAME,
                                     Config.POSTGRE_PASSWORD,
                                     Config.POSTGRE_DATABASE
                                     )
        DatabaseManager.meta_connector.setup_database()
        assert isinstance(DatabaseManager.meta_connector, PostgreSQLAlchemyConnector)


    def test_create_session(self):
        session_registry = DatabaseManager.meta_connector.create_session()
        assert isinstance(session_registry, scoped_session)

        session = session_registry()
        assert isinstance(session, Session)

        session_registry.remove()
'''