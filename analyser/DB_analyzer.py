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
MAXIMUM_QUERY = 600
MACHINE_NO = 0
MACHINE_TOTAL = 1
DB_USERNAME = 'cluster'
DB_PASSWORD = 'cluster12'
IP = '115.146.95.253'
PORT = 5984
DB_URL = 'http://%s:%s@%s:%d/tweets/' % \
         (DB_USERNAME, DB_PASSWORD, IP, PORT)

while True:
    try:
        f = open('info_analyzer.para', 'r')
        PARA = f.readlines()
        MACHINE_NO = int(PARA[0])
        MACHINE_TOTAL = int(PARA[1])
        MAXIMUM_QUERY = int(PARA[2])
        INTERVAL = int(PARA[3])
        IP = str(PARA[4]).strip('\n')
        PORT = int(PARA[5])
        DB_URL = 'http://%s:%s@%s:%d/tweets/' % \
                 (DB_USERNAME, DB_PASSWORD, IP, PORT)
        f.close()
    except:
        print('Incorrect file: info_analyzer.para')
    print('DB_URL:\t', DB_URL)
    print('MACHINE_NO:\t', MACHINE_NO)
    print('MACHINE_TOTAL:\t', MACHINE_TOTAL)
    print('MAXIMUM_QUERY:\t', MAXIMUM_QUERY)
    print('INTERVAL:  \t', INTERVAL)
    
    r = requests.get(DB_URL + '_design/analyser/_view/to_analyse')
    #L = json.loads(str(r.content))
    L = r.json()

    total_rows = L['total_rows']

    if total_rows == 0:
        print('++Nothing to be updated...++')

    D_final = {}
    D_final['docs'] = []
    
    R_final = {}
    R_final['docs'] = []

    sid = SentimentIntensityAnalyzer()

    for data_index in range(MACHINE_NO, \
                min(total_rows, MAXIMUM_QUERY * MACHINE_TOTAL), MACHINE_TOTAL):
        doc = L['rows'][data_index]['value']
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
                continue
                
        elif doc['keyword'] == 'C#':
            msg = doc['msg'].lower()
            if 'c#' not in msg or 'cs' not in msg:
                R_final['docs'].append(doc)
                continue

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
    # Delete irrelevant tweets
    for doc in R_final['docs']:
        url = DB_URL + '%s?rev=%s' % (doc['_id'], doc['_rev'])
        print('Deleting: ' + url)
        r = requests.delete(url)
        if ('ok' not in r.json()):
            print(r.json())
    time.sleep(INTERVAL)
    

        
            

