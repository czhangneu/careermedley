from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Date

import sys
import StringIO

filename = "database.config"
config_file = open(filename, 'r')
line = config_file.readline()
exec line
config_file.close()

Base = declarative_base()

class Position(Base):
    __tablename__ = 'position'

    id = Column(Integer, primary_key=True)
    #employerid = Column(Integer)
    employer_name = Column(String)
    title = Column(String)
    city = Column(String)
    state = Column(String)
    short_desc = Column(String)
    post_date = Column(Date)
    url = Column(String)
    jobkey = Column(String)
    expired = Column(String)
    deadline = Column(String)

    def __repr__(self):
        return
#
# Base.metadata.create_all(engine)
# Session = sessionmaker()
# Session.configure(bind=engine)
#     #Base.metadata.create_all(engine)
# session = Session()
#
# # position_entry = Position(employer_name = "Google1", title = "SDET",
# #                                   city = "Boston", state = "MA", short_desc = "software engineer",
# #                                   post_date = "Wed 30 July 2014", url = "http://", jobkey = "3345",
# #                                   expired = "False", deadline = 'unknown')
# #
# # session.add(position_entry)
# session.commit()
# session.close()



