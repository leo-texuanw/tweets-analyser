import requests
import json
import time
import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Parameter(s) for the sentiment classifier
NEG_THRESHOLD = 0.05

# Parameter(s) for DB request
INTERVAL = 5
DB_USERNAME = 'cluster'
DB_PASSWORD = 'cluster12'
DB_URL = 'http://%s:%s@115.146.95.253:5984/tweets/' % (DB_USERNAME, DB_PASSWORD)

while True:

    r = requests.get(DB_URL + '_design/analyser/_view/to_analyse')
    L = json.loads(r.content)

    total_rows = L['total_rows']

    if total_rows == 0:
        print('++Nothing to be updated...++')

    D_final = {}
    D_final['docs'] = []

    sid = SentimentIntensityAnalyzer()

    for data_index in range(0, total_rows):
        doc = L['rows'][data_index]['value']

        msg = doc['msg']
        print(msg.encode('ascii', 'ignore'))
        
        ss = sid.polarity_scores(msg)
        
        if ss['neg'] > ss['pos'] and ss['neg'] > NEG_THRESHOLD:
            doc['sentiment'] = 'neg'
            print('Sentiment: neg')
        else:
            doc['sentiment'] = 'pos'
            print('Sentiment: pos')

        D_final['docs'].append(doc)


    # Update DB
    r = requests.post(DB_URL + '_bulk_docs', json = D_final)
    print('Total rows:', total_rows)
    time.sleep(INTERVAL)
    

        
            

