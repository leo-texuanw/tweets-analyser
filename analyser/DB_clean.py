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

sid = SentimentIntensityAnalyzer()

for data_index in range(0, L['total_rows']):
    doc = L['rows'][data_index]['doc']

    if 'info' in doc:
        raw_str = doc['info'].encode('ascii', 'ignore').decode() 

        # find the msg range in the json string
        index_msg = str(raw_str).index('''"msg":"''') + len('''"msg":"''')
        index_end = str(raw_str)[index_msg:].index('''","''')

        prod_msg = str(raw_str)[index_msg:][:index_end].replace('''"''', '\\"', 140)
        
        #msg = re.findall('''\"msg\"\:\"([^\"]*)\"''', str(raw_str))[0]
        raw_str = str(raw_str)[:index_msg] + \
                  str(raw_str)[index_msg+index_end:]
        
        raw_json = json.loads(str(raw_str))
        raw_json['msg'] = prod_msg
        msg = raw_json['msg']
        
        ss = sid.polarity_scores(msg)
        if ss['neg'] > ss['pos'] and ss['neg'] > NEG_THRESHOLD:
            raw_json['sentiment'] = 'neg'
            print('Sentiment: neg')
        else:
            raw_json['sentiment'] = 'pos'
            print('Sentiment: pos')

        raw_json['_id'] = doc['_id']
        raw_json['_rev'] = doc['_rev']
        doc = raw_json
        print('====info====')
    
    if 'location' not in doc:
        doc['location'] = doc['location filter']
        doc.pop('location filter', None)

    D_final['docs'].append(doc)


# Update DB
r = requests.post(DB_URL + '/_bulk_docs', json = D_final)
print('Total rows:', total_rows)

    
        

