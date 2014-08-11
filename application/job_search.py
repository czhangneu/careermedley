__author__ = 'onyeka'
import json
from indeed import IndeedClient

class ProcessJobSearch():
    def __init__(self):
        print "ProcessJobSearch initialized"

    def job_search(self, job, location):
        # publisher=5950869068484812
        client = IndeedClient('5950869068484812')

        #params = generate_advanced_query("python", "Boston", 1, 0, 25)
        params = self.generate_advanced_query(job, location, 1, 0, 25)
        search_response = client.search(**params)
        print "Search Response: %s" % search_response

        filename = 'indeed_positions_json.txt'
        self.write_json_to_file(filename, search_response)


        (positions, total) = self.extract_query_result(search_response)
        print total

        jobkeys = []
        for position in positions:
            self.extract_position_info(position, jobkeys)

        #for i in range(len(jobkeys)):
            #print "range (%d: %s)" % (i, jobkeys[i])

            #print '*' * 100
            #job_response = client.jobs(jobkeys = "ad752ce9ae3f1b5e")
            #print job_response['results']
            #print job_response
            #filename = 'indeed_positions_json.txt'
            #self.write_json_to_file(filename, job_response)
        return jobkeys


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
    def generate_advanced_query(self, query_string, location, fromage, start, limit):
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
    def write_json_to_file(self, filename, search_response):
        #print search_response['results']
        # use JSON editor online to view result
        # http://www.jsoneditoronline.org/
        with open(filename, 'w') as outfile:
            json.dump(search_response, outfile)
        return

# *****************************************************************************
    def extract_query_result(self, search_response):
        for key, value in search_response.iteritems():
            print "%s: %s" % (key, value)
            if key == "results":
                positions = value
            elif key == "totalResults":
                total = int(value)
        return (positions, total)

# *****************************************************************************
# input:
# position: a dictionary
    #def extract_position_info(self, position, jobkeys):
        #print res[i]
        #for key, value in position.iteritems():
            #print "%s: %s" % (key, value)
            #if key == "jobkey":
            #    jobkeys.append(value)
# position: a dictionary
    def extract_position_info(self, position, jobkeys):
        for key, value in position.iteritems():
            #print "%s: %s" % (key, value)
            if key == 'jobkey':
                jobkeys.append({'jobkey'  : position['jobkey'],
                                'jobtitle': position['jobtitle'],
                                'company' : position['company'],
                                'city'    : position['city'],
                                'state'   : position['state'],
                                'snippet': position['snippet']})
# *****************************************************************************
