import json
from indeed import IndeedClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Positions

engine = create_engine('sqlite:///jobs.db', echo=True)

# create  a session
Session = sessionmaker(bind=engine)
session = Session()

# publisher=5950869068484812
client = IndeedClient('5950869068484812')
params = {
    'q': "python",
    'l': "Palo Alto",
    'userip': "168.159.213.210",
    'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4)",
    'limit': "50",
    'sort': "date",
    'start': "0"
}
search_response = client.search(**params)
print search_response
# print search_response['results']
# use JSON editor online to view result
# http://www.jsoneditoronline.org/

with open('indeed_positions_json.txt', 'w') as outfile:
    jobs = json.dump(search_response, outfile)
    #jobs = json.load(search_response)

for key, value in search_response.iteritems():
    #print "%s: %s" % (key, value)
    if key == "results":
        res = value
        for index in value:
            #print i
            #print index['jobkey'], "\t", index['jobtitle'], "\t",  index['url']

<<<<<<< HEAD
#print res
jobkeys = []
for i in range(len(res)):
    #print res[i]
    for key, value in res[i].iteritems():
        if key == "jobkey":
            jobkeys.append(value)

for i in range(len(jobkeys)):
    print jobkeys[i]
=======
            # add data to table
            newPosition = Positions(index['jobkey'], index['jobtitle'], index['url'])
            session.add(newPosition)
            session.commit()
>>>>>>> FETCH_HEAD

# display database row entries
#print session.query(Positions.job_title)
