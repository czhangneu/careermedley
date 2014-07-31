from sqlalchemy import *
#engine = create_engine('postgresql://scott:tiger@localhost:5432/mydatabase')
db = create_engine('postgresql+psycopg2://postgres:Sybil1101mit2013@localhost:5432/dvdsales')
# to be change
metadata = MetaData(db)
# The users table already exists, so no need to redefine it. Just
# load it from the database using the "autoload" feature.
categories = Table('categories', metadata, autoload=True)
cust_hist = Table('cust_hist', metadata, autoload=True)

def run(stmt):
    rs = stmt.execute()
    for row in rs:
        print row

s1 = select([func.count("*")], from_obj=[cust_hist])
s2 = select([func.count("*")], from_obj=[categories])
run(s2)
# s = select([categories.category, categories.categoryname])
# run(s)