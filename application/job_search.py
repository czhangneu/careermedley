__author__ = 'onyeka'
import json
from config import PUBLISHER
from indeedapi import IndeedClient

# *****************************************************************
# Class: ProcessJobSearch
# Description: Processes job search requests using the indeed API
# Params: None
# *****************************************************************
class ProcessJobSearch():
    def __init__(self):
        self.debug = 0
        print "ProcessJobSearch initialized"

    # *****************************************************************
    # Method: job_search
    # Description: Search for jobs by keyword and location
    # Params: keyword, location
    # *****************************************************************
    def job_search(self, keyword, location):
        client = IndeedClient(PUBLISHER)

        params = self.generate_advanced_query(keyword, location)
        search_response = client.search(**params)
        print "Search Response: %s" % search_response

        if (self.debug == 1):
            filename = 'indeed_positions_json.txt'
            self.write_json_to_file(filename, search_response)

        (positions, total) = self.extract_query_result(search_response)
        print total

        # get some information about the position(s)
        positions_info = self.extract_all_positions_info(positions)

        return positions_info

    # *****************************************************************
    # Method: extract_all_positions_info
    # Description: get information from all positions
    # Params: keyword, location
    # *****************************************************************
    def extract_all_positions_info(self, positions):
        positions_info = []
        for position in positions:
            self.extract_position_info(position, positions_info)
        return positions_info

    # *****************************************************************
    # Method: generate_advanced_query
    # Description: set query params
    # Params:
    # query_string: e.g. "python"
    # location: e.g. "Palo Alto"
    # days: (# Number of days back to search): e.g. 30, within 30 days
    # start: (the beginning position number of this query): e.g. 0
    # limit: (maximum number of results returned per query): e.g. 25
    # *****************************************************************
    def generate_advanced_query(self, query_string, location, days=1, start=0, limit=25):
        params = {
            'q': query_string,
            'l': location,
            'userip': "168.159.213.210",
            'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4)",
            'sort': "date",
            'fromage': str(days),  # Number of days back to search
            'start': str(start),
            'limit': str(limit)
        }
        return params

    # *****************************************************************
    # Method: write_json_to_file
    # Description: write results to a file
    # Params: filename, search_response
    # *****************************************************************
    def write_json_to_file(self, filename, search_response):
        # print search_response['results']
        # use JSON editor online to view result
        # http://www.jsoneditoronline.org/
        with open(filename, 'w') as outfile:
            json.dump(search_response, outfile)
        return

    # *****************************************************************
    # Method: extract_query_result
    # Description: get positions from query results
    # Params: search_response
    # *****************************************************************
    def extract_query_result(self, search_response):
        positions = None
        total = 0
        for key, value in search_response.iteritems():
            #print "%s: %s" % (key, value)
            if key == "results":
                positions = value
                total = total + 1
            elif key == "totalResults":
                total = int(value)
        return (positions, total)

    # *****************************************************************
    # Method: extract_position_info
    # Description: extract some information from position
    # Params: position, position_info
    # *****************************************************************
    def extract_position_info(self, position, position_info):
        for key, value in position.iteritems():
            # print "Key: %s: Value: %s" % (key, value)
            if key == 'jobkey':
                position_info.append({'jobkey': position['jobkey'],
                                      'jobtitle': position['jobtitle'],
                                      'date' : position['date'],
                                      'company': position['company'],
                                      'city': position['city'],
                                      'state': position['state'],
                                      'url': position['url'],
                                      'snippet': position['snippet'],
                                      'expired': position['expired']})

    # *****************************************************************
    # Method: generate_job_query
    # Description: set query parameters for searching for a single job
    # Params: jobkeys
    # *****************************************************************
    def generate_job_query(self, jobkeys):
        params = {
            'jobkeys': str(jobkeys)
        }
        return params

    # *****************************************************************
    # Method: search_by_jobkeys
    # Description: for positions by jobkey
    # Params: jobkeys
    # *****************************************************************
    def search_by_jobkeys(self, jobkeys):
        client = IndeedClient(PUBLISHER)
        params = self.generate_job_query(jobkeys)
        #print " params are: %s" % params
        search_response = client.jobs(**params)
        print "search response: %s" % search_response
        (positions, total) = self.extract_query_result(search_response)

        # get some information about the position(s)
        positions_info = self.extract_all_positions_info(positions)

        return positions_info