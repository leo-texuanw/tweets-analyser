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
    REV = [i['value']['rev'] for i in L['rows']]

    if len(UID) == 0:
        print('Warning: %s is empty.' % db_name)
        continue
    
    L = []

    # Get all items in the sub_db by uid
    for data_index in range(0, len(UID)):
        uuid = UID[data_index]
        rrev = REV[data_index]
        
        url = DB_URL + db_name + '/'+str(uuid)
        print(url)
        r = requests.get(url)
        L.append(r.json())

        json_dict = L[-1]
        
        if not json_dict:
            continue
        elif 'info' in json_dict:
            raw_str = json_dict['info'].encode('ascii', 'ignore').decode() 

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
            lang_dict[db_name]['total'] += 1
            if ss['neg'] > ss['pos'] and ss['neg'] > NEG_THRESHOLD:
                lang_dict[db_name]['neg'] += 1
                raw_json['sentiment'] = 'neg'
                print('Sentiment: neg')
            else:
                lang_dict[db_name]['pos'] += 1
                raw_json['sentiment'] = 'pos'
                print('Sentiment: pos')

            raw_json['_id'] = uuid
            raw_json['_rev'] = rrev
            
            print(raw_json)


            # Update DB
            r = requests.put(url, json.dumps(raw_json))
            if not r.json()['ok']:
                print('#'*20 + ' ERROR ' + '#'*20)
                print(r.json())
            
