from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
#engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
engine = create_engine('postgresql+psycopg2://postgres:Sybil1101mit2013@localhost:5432/dvdsales', echo=True)


# ------------------------------------------------------------
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)

    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')" % (self.name, self.fullname, self.password)
#
# Base.metadata.create_all(engine)
# ------------------------------------------------------------
# after creating the table, comment the above code

from sqlalchemy.orm import sessionmaker
Session = sessionmaker(bind=engine)
Session.configure(bind=engine)
session = Session()

# ed_user = User(name='ed', fullname='Ed Jones', password='edspassword')
# print ed_user.name
# print ed_user.password
#
# session.add(ed_user)
#
# our_user = session.query(User).filter_by(name='ed').first()
# print our_user
#
# print ed_user is our_user
#
# session.add_all(
#     [
#         User(name='Wendy', fullname='Wendy Williams', password='foobar'),
#         User(name='Mary', fullname='Mary Contrary', password='xxg527')
#     ]
# )
#
# ed_user.password = 'f8s7ccs'
#session.commit()

# print ed_user.id

# for instance in session.query(User).order_by(User.id):
#     print instance.name, instance.fullname

# for name, fullname in session.query(User.name, User.fullname):
#     print name, fullname

#for row in session.query(User, User.name).all():
for row in session.query(User, User.name).all():
    print row.User, row.name

