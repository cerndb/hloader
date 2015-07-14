from hloader.db.connectors.sqlaentities.Base import Base
from hloader.entities.HadoopCluster import HadoopCluster
from hloader.entities.Job import Job
from hloader.entities.OracleServer import OracleServer

__author__ = 'dstein'

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Interval
from sqlalchemy.orm import relationship


class Job(Base, Job):
    __tablename__ = "HL_JOBS"

    job_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)  # SERIAL NOT NULL,
    source_server_id = Column(Integer, ForeignKey('HL_SERVERS.server_id'), nullable=False)  # INTEGER NOT NULL ,
    source_database_name = Column(String, nullable=False)  # TEXT NOT NULL ,
    source_table_name = Column(String, nullable=False)  # TEXT NOT NULL ,
    destination_cluster_id = Column(Integer, ForeignKey('HL_CLUSTERS.cluster_id'), nullable=False)  # INTEGER NOT NULL ,
    destination_path = Column(String, nullable=False)  # TEXT NOT NULL ,
    query_columns = Column(String, nullable=False)  # TEXT NOT NULL ,
    query_source = Column(String, nullable=False)  # TEXT NOT NULL ,
    query_conditions = Column(String, nullable=False)  # TEXT NOT NULL ,
    sqoop_nmap = Column(Integer)  # INTEGER ,
    sqoop_splitting_column = Column(String)  # TEXT ,
    sqoop_incremental_method = Column(String)  # TEXT ,
    sqoop_direct = Column(Boolean, nullable=False)  # INTEGER NOT NULL ,
    start_time = Column(DateTime(timezone=True), nullable=False)  # INTEGER NOT NULL,
    interval = Column(Interval, nullable=False)  # INTEGER NOT NULL

    source_server = relationship("hloader.db.connectors.sqlaentities.OracleServer.OracleServer")
    destination_cluster = relationship("hloader.db.connectors.sqlaentities.HadoopCluster.HadoopCluster")
    transfers = relationship("hloader.db.connectors.sqlaentities.Transfer.Transfer")

    def get_source_server(self) -> OracleServer:
        return super().get_source_server()

    def get_destination_cluster(self) -> HadoopCluster:
        return super().get_destination_cluster()
