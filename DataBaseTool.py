__author__ = 'www.showbt.com'

# -*- coding:utf-8 -*-

from sqlalchemy import Column, String, create_engine, Text, Integer, ForeignKey
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class ModelInfo(Base):
    __tablename__ = 'tb_model_info'

    id = Column(String(36), primary_key=True)
    name = Column(String(20))
    info = Column(Text())
    topPic = Column(String(100))
    age = Column(String(4))
    url = Column(String(100))
    local = Column(String(50))


class ModelImage(Base):
    __tablename__ = 'tb_model_img'

    id = Column(String(36), primary_key=True)
    imgurl = Column(String(400))
    # , ForeignKey('tb_model_info.id', ondelete='CASCADE', onupdate='CASCADE')
    miid = Column(String(36))


class DataBaseTool(object):
    def __init__(self):
        self.DB_CONNECT_STRING = 'mysql+mysqldb://root:root@localhost/python_test?charset=utf8'
        self.engine = create_engine(self.DB_CONNECT_STRING, echo=False)
        # self.session = sessionmaker(bind=self.engine)

        self.DB_Session = scoped_session(sessionmaker(autoflush=True, bind=self.engine))
        self.session = self.DB_Session()

    def create_db(self):
        Base.metadata.create_all(self.engine)

    def drop_db(self):
        Base.metadata.drop_all(self.engine)

    def get_session(self):
        return self.session

    def close_session(self, session):
        session.close()
        self.DB_Session.remove()
