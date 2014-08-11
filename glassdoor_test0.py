from glassdoor import get
# *****************************************************************************
def extract_fields(response):
    satisfaction, ceo, meta, salary = None, None, None, None
    for key, value in response.iteritems():
        if key == 'satisfaction':
            satisfaction = value
        elif key == 'ceo':
            ceo = value
        elif key == 'meta':
            meta = value
        elif key == 'salary':
            salary = value
    return (satisfaction, ceo, meta, salary)
# *****************************************************************************
def extract_satisfaction(satisfaction):
    numRatings, score = None, None
    for key, value in satisfaction.iteritems():
        if key == 'ratings':
            numRatings = value
        elif key == 'score':
            score = value
    return (numRatings, score)
# *****************************************************************************
def extract_ceo(ceo):
    numReviews, approvalRate, name, avatarLink = None, None, None, None
    for key, value in ceo.iteritems():
        if key == 'reviews':
            numReviews = value
        elif key == '%approval':
            approvalRate = value
        elif key == 'name':
            name = value
        elif key == 'avatar':
            avatarLink = value
    return (numReviews, approvalRate, name, avatarLink)
# *****************************************************************************

def main():
    #response = get('dropbox')
    #response = get('The Bowdoin Group')
    response = get('dropbox')
    #print x
    for key, value in response.iteritems():
       print "(%s: %s)" % (key, value)
    (satisfaction, ceo, meta, salary) = extract_fields(response)
    (numRatings, score) = extract_satisfaction(satisfaction)
    print numRatings, score

if __name__ == '__main__':
    main()