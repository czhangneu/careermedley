__author__ = 'onyekaigabari'

from sqlalchemy import create_engine, Table, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# initialize db connection
engine = create_engine('sqlite:///jobs.db', echo=True)
Base   = declarative_base()

# db Class
class Positions(Base):
    __tablename__ = 'positions'
    id = Column(Integer, primary_key=True)
    job_id    = Column(String(50), unique=True)
    job_title = Column(String(100))
    job_link  = Column(String(500))

    def __init__(self, id, title, link):
        self.job_id    = id
        self.job_title = title
        self.job_link  = link

# create tables
Base.metadata.create_all(engine)

