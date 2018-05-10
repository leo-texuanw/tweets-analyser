import requests
import json
import re
import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle

# Parameter(s) for the sentiment classifier
NEG_THRESHOLD = 0.05

# Parameter(s) for DB request
DB_USERNAME = 'cluster'
DB_PASSWORD = 'cluster12'
DB_URL = 'http://%s:%s@115.146.95.198:5985/' % (DB_USERNAME, DB_PASSWORD)
INFO_DB_NAME = '#sentiment_info'

# Load trained classifier
'''
f = open('twitter_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()
'''

# Get all DBs
r = requests.get(DB_URL + '_all_dbs')
all_dbs = r.json()

sid = SentimentIntensityAnalyzer()
lang_dict = {}

for db_name in all_dbs:
    # Detect if the DB is the (reserved) info DB
    if db_name == INFO_DB_NAME:
        continue

    
    print('>'*20 + db_name + '<'*20 )
    lang_dict[db_name] = {'pos': 0, 'neg': 0, 'total': 0}
    
    r = requests.get(DB_URL + '%s/_all_docs' % \
                     db_name)
    L = json.loads(r.content)

    UID = [i['id'] for i in L['rows']]

    if len(UID) == 0:
        print('Warning: %s is empty.' % db_name)
        continue
    
    L = []

    # Get all items in the sub_db by uid
    for uuid in UID:
        url = DB_URL + db_name + '/'+str(uuid)
        #print(url)
        r = requests.get(url)
        L.append(r.json())

        json_dict = L[-1]
        
        if json_dict:
            raw_str = json_dict['info'].encode('ascii', 'ignore')
            msg = re.findall('''\"msg\"\:\"([^\"]*)\"''', str(raw_str))[0]
            #msg = json.loads(L[-1]['info'].encode('ascii', 'ignore'))['msg']
            
            ss = sid.polarity_scores(msg)
            lang_dict[db_name]['total'] += 1
            if ss['neg'] > ss['pos'] and ss['neg'] > NEG_THRESHOLD:
                lang_dict[db_name]['neg'] += 1
                json_dict['sentiment'] = 'neg'
                print('Sentiment: neg')
            else:
                lang_dict[db_name]['pos'] += 1
                json_dict['sentiment'] = 'pos'
                print('Sentiment: pos')

            # Update DB
            r = requests.put(url, json.dumps(json_dict))
            if not r.json()['ok']:
                print('#'*20 + ' ERROR ' + '#'*20)
                print(r.json())
                
