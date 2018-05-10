import requests
import json
import re
import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Parameter(s) for the sentiment classifier
NEG_THRESHOLD = 0.05

# Parameter(s) for DB request
DB_USERNAME = 'cluster'
DB_PASSWORD = 'cluster12'
DB_URL = 'http://%s:%s@115.146.95.253:5984/tweets/' % (DB_USERNAME, DB_PASSWORD)

r = requests.get(DB_URL + '_all_docs?include_docs=true')
L = json.loads(r.content)


total_rows = L['total_rows']

if total_rows == 0:
    print('Warning: %s is empty.' % db_name)

D_final = {}
D_final['docs'] = []

R_final = {}
R_final['docs'] = []

sid = SentimentIntensityAnalyzer()

for data_index in range(0, total_rows):
    doc = L['rows'][data_index]['doc']
    if 'msg' not in doc:
        continue
    if 'keyword' not in doc:
        msg = doc['msg'].lower()
        if 'python' in msg:
            doc['keyword'] = 'Python'
        elif 'java ' in msg:
            doc['keyword'] = 'Java'
        elif ' C++ ' in msg:
            doc['keyword'] = 'C++'
        elif 'javascript' in msg:
            doc['keyword'] = 'JavaScript'
        elif 'haskell' in msg:
            doc['keyword'] = 'Haskell'
        elif 'php' in msg:
            doc['keyword'] = 'PHP'
        elif ' sql ' in msg:
            doc['keyword'] = 'SQL'
        else:
            R_final['docs'].append(doc)
            continue
        
        D_final['docs'].append(doc)

    elif doc['keyword'] == 'C++':
        msg = doc['msg'].lower()
        msg = ' ' + msg + ' '
        if 'c++' not in msg or ' cpp' not in msg:
            R_final['docs'].append(doc)
    elif doc['keyword'] == 'C#':
        msg = doc['msg'].lower()
        if 'c#' not in msg or 'cs' not in msg:
            R_final['docs'].append(doc)

    print(data_index)


# Update DB
r = requests.post(DB_URL + '/_bulk_docs', json = D_final)
print('Total rows:', len(D_final['docs']))

for doc in R_final['docs']:
    url = DB_URL + '%s?rev=%s' % (doc['_id'], doc['_rev'])
    print('Deleting: ' + url)
    r = requests.delete(url)
    if ('ok' not in r.json()):
        print(r.json())

    
        

