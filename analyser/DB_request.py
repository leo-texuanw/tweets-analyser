import requests
import json
import re
import nltk
from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pickle

# Parameter(s) for the sentiment classifier
NEG_THRESHOLD = 0.1

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
    # Detect if the DB is the (researved) info DB
    if db_name == INFO_DB_NAME:
        continue
    
    lang_dict[db_name] = {'pos': 0, 'neg': 0, 'total': 0}
    
    r = requests.get(DB_URL + '%s/_all_docs' % \
                     db_name)
    L = json.loads(r.content)

    UID = [i['id'] for i in L['rows']]

    if len(UID) == 0:
        print('Warning: %s is empty.' % db_name)
        continue
    
    L = []

    for uuid in UID[:100]:
        url = DB_URL + db_name + '/'+str(uuid)
        print(url)
        r = requests.get(url)
        L.append(r.json())
        if 1:
            raw_str = L[-1]['info'].encode('ascii', 'ignore')
            msg = re.findall('''\"msg\"\:\"([^\"]*)\"''', str(raw_str))[0]
            #msg = json.loads(L[-1]['info'].encode('ascii', 'ignore'))['msg']
            
            ss = sid.polarity_scores(msg)
            lang_dict[db_name]['total'] += 1
            if ss['neg'] > ss['pos'] and ss['neg'] > NEG_THRESHOLD:
                lang_dict[db_name]['neg'] += 1
                print(msg)
                print(ss, end = '\n\n')
            else:
                lang_dict[db_name]['pos'] += 1
                
