from hloader.db.connectors.sqlaentities.Base import Base
from hloader.entities.Log import Log

__author__ = 'dstein'

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Log(Base, Log):
    __tablename__ = "HL_LOGS"

    log_id = Column(Integer, autoincrement=True, nullable=False, primary_key=True)  # SERIAL NOT NULL,
    transfer_id = Column(Integer, ForeignKey('HL_TRANSFERS.transfer_id'), nullable=False)  # INTEGER NOT NULL ,
    log_source = Column(String, nullable=False)  # TEXT NOT NULL
    log_path = Column(String, nullable=True)
    log_content = Column(String, nullable=True)

    transfer = relationship("hloader.db.connectors.sqlaentities.Transfer.Transfer")
