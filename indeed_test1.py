import json
from indeed import IndeedClient

def main():
    # publisher=5950869068484812
    client = IndeedClient('5950869068484812')

    params = generate_advanced_query("python", "Boston", 1, 0, 25)
    search_response = client.search(**params)
    #print search_response

    filename = 'indeed_positions_json.txt'
    write_json_to_file(filename, search_response)


    (positions, total) = extract_query_result(search_response)
    print total

    jobkeys = []
    for position in positions:
        extract_position_info(position, jobkeys)

    for i in range(len(jobkeys)):
        print "(%d: %s)" % (i, jobkeys[i])

    print '*' * 100
    job_response = client.jobs(jobkeys = "ad752ce9ae3f1b5e")
    #print job_response['results']
    print job_response
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
        # print "%s: %s" % (key, value)
        if key == "jobkey":
            jobkeys.append(value)
# *****************************************************************************


if __name__ == "__main__":
    main()