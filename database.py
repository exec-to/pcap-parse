# -*- coding: UTF-8 -*-
import config
import sqlalchemy as db
from sqlalchemy import Table, Column, Integer, String, MetaData, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import mapper
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Входящий трафик, объём по ip:port в секунду, PPS, bytes
class Incoming(Base):
    __tablename__ = 'incoming'
    id = Column('id', Integer, primary_key=True)
    # timestamp = Column(DateTime, nullable=False)
    dst = Column(String(20), nullable=False)
    dport = Column(Integer, nullable=False)
    packets = Column(Integer, nullable=False)
    bytes = Column(Integer, nullable=False)

    def __init__(self, dst, dport, packets, packet_len):
        self.dst = dst
        self.dport = dport
        self.packets = packets
        self.bytes = packet_len


class Db:
    def __init__(self):
        self.engine = db.create_engine(
            'mysql+mysqlconnector://{user}:{passwd}@{host}:{port}/{db}'
            .format_map(config.database),
            echo=False,
            connect_args={'connect_timeout': 10}
        )

        Base.metadata.create_all(self.engine)
