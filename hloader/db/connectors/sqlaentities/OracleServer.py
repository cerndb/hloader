from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from hloader.db.connectors.sqlaentities.Base import Base
from hloader.entities.OracleServer import OracleServer


class OracleServer(Base, OracleServer):
    __tablename__ = "hl_servers"

    server_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)  # SERIAL NOT NULL,
    server_address = Column(String, nullable=False)  # TEXT NOT NULL ,
    server_port = Column(Integer, nullable=False)  # INTEGER NOT NULL ,
    server_service = Column(String, nullable=False)  # TEXT NOT NULL,
    server_name = Column(String, nullable=False)  # TEXT NOT NULL

    jobs = relationship("hloader.db.connectors.sqlaentities.Job.Job")
