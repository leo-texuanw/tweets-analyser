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
DB_URL = 'http://%s:%s@115.146.95.198:5985/' % (DB_USERNAME, DB_PASSWORD)
INFO_DB_URL = 'http://%s:%s@115.146.95.253:5984/tweets/' % (DB_USERNAME, DB_PASSWORD)

# Get all DBs
r = requests.get(DB_URL + '_all_dbs')
all_dbs = r.json()
total_rows = 0

sid = SentimentIntensityAnalyzer()
lang_dict = {}
lang_rebase = {'java_res': 'Java', 'cpp_res': 'C++',\
               'cppprogram_res': 'C++', 'sql_res': 'SQL',\
               'cs_res': 'C#', 'haskell_res': 'Haskell',\
               'javascript_res': 'JavaScript', 'php_res': 'PHP',\
               'prolog_res': 'Prolog', 'python_res': 'Python',\
               'matlab_res': 'MATLAB'}

for db_name in all_dbs:
    
    print('>'*20 + db_name + '<'*20 )
    lang_dict[db_name] = {'pos': 0, 'neg': 0, 'total': 0}
    
    r = requests.get(DB_URL + '%s/_all_docs?include_docs=true' % \
                     db_name)
    L = json.loads(r.content)

    if L['total_rows'] == 0:
        print('Warning: %s is empty.' % db_name)
        continue

    total_rows += L['total_rows']
    D_final = {}
    D_final['docs'] = []

    # Get all items in the sub_db by uid
    for data_index in range(0, L['total_rows']):
        doc = L['rows'][data_index]['doc']
        doc.pop('_rev', None)
        doc['retweeted'] = False
        if 'keyword' not in doc:
            doc['keyword'] = lang_rebase[db_name]

        D_final['docs'].append(doc)
        
    # Update DB
    url = INFO_DB_URL + doc['_id']
    r = requests.post(INFO_DB_URL + '/_bulk_docs', json = D_final)
    print('Total rows:', total_rows)
        
            
