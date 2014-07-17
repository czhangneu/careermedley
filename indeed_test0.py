import json
from indeed import IndeedClient

# publisher=5950869068484812
client = IndeedClient('5950869068484812')
params = {
    'q': "python",
    'l': "Palo Alto",
    'userip': "168.159.213.210",
    'useragent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_4)",
    'limit':"50",
    'sort':"date",
    'start':"0"
}
search_response = client.search(**params)
#print search_response
#print search_response['results']
# use JSON editor online to view result
# http://www.jsoneditoronline.org/

with open('indeed_positions_json.txt', 'w') as outfile:
    json.dump(search_response, outfile)

for key, value in search_response.iteritems():
    print "%s: %s" % (key, value)
    if key == "results":
        res = value

print res


