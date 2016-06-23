from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from hloader.db.connectors.sqlaentities.Base import Base
from hloader.entities.HadoopCluster import HadoopCluster


class HadoopCluster(Base, HadoopCluster):
    __tablename__ = "hl_clusters" #postgres convention for names is lower case

    cluster_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)  # SERIAL NOT NULL,
    cluster_address = Column(String, nullable=False)  # TEXT NOT NULL ,
    cluster_name = Column(String, nullable=False)  # TEXT NOT NULL

    jobs = relationship("hloader.db.connectors.sqlaentities.Job.Job")
