# test batch populating position entries to table: position
import json
from indeed import IndeedClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from careermedley_database_generation import Position
import sys
import StringIO

def main():
    # publisher=5950869068484812
    client = IndeedClient('5950869068484812')

    params = generate_advanced_query("python", "Boston", 1, 0, 25)
    search_response = client.search(**params)
    #print search_response

    filename = 'indeed_positions_json.txt'
    write_json_to_file(filename, search_response)

    # ask Indeed to provide positions
    (positions, total) = extract_query_result(search_response)
    print total

    jobkeys = []

    #
    filename = "database.config"
    config_file = open(filename, 'r')
    line = config_file.readline()
    exec line
    config_file.close()


    Session = sessionmaker()
    Session.configure(bind=engine)
    #Base.metadata.create_all(engine)
    session = Session()

    #
    cnt = 0
    for position in positions:
        # write to database
        # extract_position_info(position, jobkeys)
        (employer_name, title, city, state, short_desc, post_date, url, jobkey, expired) \
            = extract_position_info(position, jobkeys)
        print "(%s, %s, %s, %s)" % (employer_name, title, city, state)


        # position_entry = Position(employer_name = "Google1", title = "SDET",
        #                           city = "Boston", state = "MA", short_desc = "software engineer",
        #                           post_date = "Wed 30 July 2014", url = "http://", jobkey = "3345",
        #                           expired = "False", deadline = 'unknown')


        position_entry = Position(employer_name = employer_name, title = title,
                                  city = str(city), state = str(state),
                                  #short_desc = str(short_desc.encode('utf-8').strip()),
                                  short_desc = short_desc,
                                  #short_desc = "software developer",
                                  #post_date = str('Wed 30 July 2014'),
                                  post_date = str(post_date),
                                  url = str(url), jobkey = str(jobkey),
                                  expired = str(expired), deadline = 'unknown')
        session.add(position_entry)

    session.commit()
    session.close()




    # for i in range(len(jobkeys)):
    #     print "(%d: %s)" % (i, jobkeys[i])


    # print '*' * 100
    # job_response = client.jobs(jobkeys = "ad752ce9ae3f1b5e")
    # #print job_response['results']
    # print job_response
    #filename = 'indeed_positions_json.txt'
    #write_json_to_file(filename, job_response)


# *****************************************************************************
# generate_advanced_query:
# ----------------------------------------------------------------
# input:
# query_string: e.g. "python"
# location: e.g. "Palo Alto"
# fromage (# Number of days back to search): e.g. 30, within 30 days
# start (the beginning position number of this query): e.g. 0
# limit (maximum number of results returned per query): e.g. 25
# ----------------------------------------------------------------
# output:
# params: used to submit to Indeed API to search
def generate_advanced_query(query_string, location, fromage, start, limit):
    params = {
    'q': query_string,
    'l': location,
    'userip': "168.159.213.210",
    'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4)",
    'sort':"date",
    'fromage': str(fromage),   # Number of days back to search
    'start': str(start),
    'limit': str(limit)
    }
    return params

# *****************************************************************************
def write_json_to_file(filename, search_response):
    #print search_response['results']
    # use JSON editor online to view result
    # http://www.jsoneditoronline.org/
    with open(filename, 'w') as outfile:
        json.dump(search_response, outfile)
    return

# *****************************************************************************
def extract_query_result(search_response):
    for key, value in search_response.iteritems():
        #print "%s: %s" % (key, value)
        if key == "results":
            positions = value
        elif key == "totalResults":
            total = int(value)
    return (positions, total)

# *****************************************************************************
# input:
# position: a dictionary
def extract_position_info(position, jobkeys):
    #print res[i]
    for key, value in position.iteritems():
        #print "%s: %s" % (key, value)
        if key == "company":
            employer_name = value
        elif key == "jobtitle":
            #print "%s: %s" % (key, value)
            title = value
        elif key == "city":
            city = value
        elif key == "state":
            state = value
        elif key == "snippet":
            short_desc = value
        elif key == "date":
            post_date = value
        elif key == "url":
            url = value
        elif key == "jobkey":
            #jobkeys.append(value)
            #print "%s: %s" % (key, value)
            jobkey = value
        elif key == "expired":
            expired = value

    return (employer_name, title, city, state, short_desc, post_date, url, jobkey, expired)

# *****************************************************************************


if __name__ == "__main__":
    main()