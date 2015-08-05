from __future__ import absolute_import

from hloader.config import POSTGRE_ADDRESS, POSTGRE_DATABASE, POSTGRE_PASSWORD, POSTGRE_PORT, POSTGRE_USERNAME

from hloader.db.DatabaseManager import DatabaseManager
from hloader.db.connectors.PostgreSQLAlchemyConnector import PostgreSQLAlchemyConnector

from sqlalchemy.orm import Session, scoped_session


class TestPostgreSQLAlchemyConnector:
    def test_setup_database(self):
        DatabaseManager.connect_meta("PostgreSQLA", POSTGRE_ADDRESS, POSTGRE_PORT, POSTGRE_USERNAME,
                                     POSTGRE_PASSWORD, POSTGRE_DATABASE)
        DatabaseManager.meta_connector.setup_database()
        assert isinstance(DatabaseManager.meta_connector, PostgreSQLAlchemyConnector)


    def test_create_session(self):
        session_registry = DatabaseManager.meta_connector.create_session()
        assert isinstance(session_registry, scoped_session)

        session = session_registry()
        assert isinstance(session, Session)

        session_registry.remove()