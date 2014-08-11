import json
from indeed import IndeedClient
from indeedapi import IndeedApi

def main():
    # publisher=5950869068484812
    client = IndeedClient('5950869068484812')

    numPositionPerPage = 25
    params = generate_advanced_query("google", "Boston", 1, 0, numPositionPerPage)
    search_response = client.search(**params)
    #print search_response

    filename = 'indeed_positions_json.txt'
    write_json_to_file(filename, search_response)


    (positions, total) = extract_query_result(search_response)
    print total
    print "number of pages: ", obtain_number_of_pages(total, numPositionPerPage)

    jobkeys = []
    for position in positions:
        extract_position_info(position, jobkeys)

    for i in range(len(jobkeys)):
        print "(%d: %s)" % (i, jobkeys[i])

    print '*' * 100

    job_response = client.jobs(jobkeys = ("fab9f8e3cc8ba41c"))
    #print job_response[u'results']
    #print job_response
    #filename = 'indeed_positions_json.txt'
    #write_json_to_file(filename, job_response)

    # token = "5950869068484812"
    # api = IndeedApi(token)
    # job_details = api.job_details(["fab9f8e3cc8ba41c"])
    #print job_details
    # for key, value in job_details.iteritems():
    #     #print key, value
    #     if key == u'results':
    result = search_by_jobkeys(["fab9f8e3cc8ba41c"])
    #print result[0]
    for key, value in result[0].iteritems():
        print "%s: %s" % (key, value)


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
        # print "%s: %s" % (key, value)
        if key == "jobkey":
            jobkeys.append(value)
# *****************************************************************************
#
# calculate how many pages there
# totresult / (num of positions per page)
def obtain_number_of_pages(totalResults, numPositionPerPage):
    numPages = (totalResults / numPositionPerPage + 1)
    return numPages

# *****************************************************************************
def search_by_jobkeys(jobkeys):
    token = "5950869068484812"
    api = IndeedApi(token)
    job_details = api.job_details(jobkeys)
    #print job_details
    result = None
    for key, value in job_details.iteritems():
        #print key, value
        if key == u'results':
            result = value
    return result

if __name__ == "__main__":
    main()