from __future__ import absolute_import
from hloader.db.connectors.sqlaentities.Base import Base
from hloader.entities.Job import Job

__author__ = 'dstein'

import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, Interval
from sqlalchemy.orm import relationship


class Job(Base, Job):
    __tablename__ = "HL_JOBS"

    job_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)  # SERIAL NOT NULL,

    source_server_id = Column(Integer, ForeignKey('HL_SERVERS.server_id'), nullable=False)  # INTEGER NOT NULL ,
    source_schema_name = Column(String, nullable=False)  # TEXT NOT NULL ,
    source_object_name = Column(String, nullable=False)  # TEXT NOT NULL ,

    destination_cluster_id = Column(Integer, ForeignKey('HL_CLUSTERS.cluster_id'), nullable=False)  # INTEGER NOT NULL ,
    destination_path = Column(String, nullable=False)  # TEXT NOT NULL ,

    owner_username = Column(String, nullable=False)  # TEXT NOT NULL ,

    sqoop_nmap = Column(Integer)  # INTEGER ,
    sqoop_splitting_column = Column(String)  # TEXT ,
    sqoop_incremental_method = Column(String)  # TEXT ,
    sqoop_direct = Column(Boolean, nullable=False)  # INTEGER NOT NULL ,

    start_time = Column(DateTime(timezone=True), default=datetime.datetime.now())
    interval = Column(Interval)

    job_last_update = Column(DateTime(timezone=True),
                             onupdate=datetime.datetime.now(),
                             default=datetime.datetime.now())  # TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP


    source_server = relationship("hloader.db.connectors.sqlaentities.OracleServer.OracleServer", lazy='joined')
    destination_cluster = relationship("hloader.db.connectors.sqlaentities.HadoopCluster.HadoopCluster", lazy='joined')
    transfers = relationship("hloader.db.connectors.sqlaentities.Transfer.Transfer")

    def get_source_server(self):
        return self.source_server

    def get_destination_cluster(self):
        return self.destination_cluster
