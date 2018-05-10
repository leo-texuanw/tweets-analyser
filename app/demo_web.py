import os
root = os.path.abspath(os.path.dirname(__file__)) + '/'

from flask import Flask, request, redirect
app = Flask(__name__, static_folder='.', static_url_path='')

import requests
import json
import pandas as pd
import numpy as np
import math
import time
# seaborn is used to output the heat map (to colour the pivot table)
#import seaborn as sns

# Define the global variables used in this programme
global index_html, home_html, map_view_html
global pivot_html, data_exp_html, html_column
global pivot_output_html, bubble_html, bubble_js
global DB_URL
global dict_axis
global dict_LCS, L_city, L_lang
global bubble_init
global dict_avg_income_pp
global dict_avg_income_ph
global dict_non_neg
global dict_num_household
global dict_num_tweets

bubble_init = False

dict_axis = {0: 'Non-negative Rate', \
             1: 'Number of Tweets', \
             2: 'Average Income per Person', \
             3: 'Average Income per Household', \
             4: 'Number of Households'}

index_html = open('index.html', 'r').read()
home_html = open('home.html', 'r').read()
map_view_html = open('map_view.html', 'r').read()

# The HTML page of Data Explorer
data_exp_html = open('data_exp.html', 'r').read()

# The HTML page of the Pivot Table Generator
pivot_output_html = open('pivot_output.html', 'r').read()

# The HTML page of the Bubble Chart Generator
bubble_html = open('bubble.html', 'r').read()


def connect_db():
    global dict_LCS, L_city, L_lang
    global DB_URL
    
    DB_USERNAME = 'cluster'
    DB_PASSWORD = 'cluster12'
    
    f = open('info_db.para', 'r')
    PARA = f.read().split('\n')
    IP = str(PARA[0]).strip('\n')
    PORT = int(PARA[1])
    DB_URL = 'http://%s:%s@%s:%d/' % \
             (DB_USERNAME, DB_PASSWORD, IP, PORT)
    f.close()
    
    STAT_URL = DB_URL + 'tweets/_design/stat/_view/city_lang?group=true'
    
    # Load statistic data from DB
    r = requests.get(STAT_URL)
    L = json.loads(r.content)['rows']

    dict_LCS = {}
    L_city = []
    L_lang = []

    for record in L:
        if record['key'][0] not in L_city:
            L_city.append(record['key'][0])
        if record['key'][1] not in L_lang:
            L_lang.append(record['key'][1])

    L_lang.sort()
    L_city.sort()

    print('Lang:', L_lang)
    print('City:', L_city)

    for lang in L_lang:
        dict_LCS[lang] = {}
        for city in L_city:
            dict_LCS[lang][city] = {'pos': 0, 'neg': 0}

    # Fill the pos and neg values
    for record in L:
        dict_LCS[record['key'][1]][record['key'][0]][record['key'][2]] = record['value']

    # Do total stats
    total_by_lang = {}
    for city in L_city:
        total_by_lang[city] = {'pos': 0, 'neg': 0}
        for lang in L_lang:
            total_by_lang[city]['pos'] += dict_LCS[lang][city]['pos']
            total_by_lang[city]['neg'] += dict_LCS[lang][city]['neg']      
    dict_LCS['Total'] = total_by_lang

    for lang in L_lang + ['Total']:
        total_by_city = {'pos': 0, 'neg': 0}
        for city in L_city:
            total_by_city['pos'] += dict_LCS[lang][city]['pos']
            total_by_city['neg'] += dict_LCS[lang][city]['neg']
        dict_LCS[lang]['Total'] = total_by_city


def bubble_data_analyzer():
    global dict_LCS, L_city, L_lang
    global bubble_init
    global dict_avg_income_pp
    global dict_avg_income_ph
    global dict_non_neg
    global dict_num_household
    global dict_num_tweets
    global DB_URL

    dict_avg_income_pp = {}
    dict_avg_income_ph = {}
    dict_non_neg = {}
    dict_num_household = {}
    dict_num_tweets = {}

    if bubble_init:
        return

    for city in L_city:
        dict_num_tweets[city] = \
            dict_LCS['Total'][city]['pos'] + dict_LCS['Total'][city]['neg']
        dict_non_neg[city] = \
            dict_LCS['Total'][city]['pos'] / dict_num_tweets[city]


    for lang in L_lang:
        dict_num_tweets[lang] = \
            dict_LCS[lang]['Total']['pos'] + dict_LCS[lang]['Total']['neg']
        dict_non_neg[lang] = \
            dict_LCS[lang]['Total']['pos'] / dict_num_tweets[lang]

    STAT_URL = DB_URL + 'aurin_db/stats'
    r = requests.get(STAT_URL)
    L = r.json()
    print(L)
    dict_avg_income_pp = L['avg_income_pp']
    dict_avg_income_ph = L['avg_income_ph']
    dict_num_household = L['num_household']

    bubble_init = True

def bubble_js_generator(mode, x_axis, y_axis, bubble_axis):
    global dict_LCS, L_city, L_lang
    global dict_avg_income_pp
    global dict_avg_income_ph
    global dict_non_neg
    global dict_num_household
    global dict_num_tweets

    global dict_axis

    if mode == 'lang':
        L_class = L_lang
    elif mode == 'city':
        L_class = L_city

    # Javascript framework of the bubble.js
    js_framework = '''var data = [%s]\n
var layout = {
  xaxis: {
    title: '%s'
  },
  yaxis: {
    title: '%s',
    type: 'log'
  },
  margin: {
    t: 20
  },
  hovermode: 'closest'
};

BUBBLE = document.getElementById('bubble');

Plotly.plot(BUBBLE, data, layout);'''
    
    # Data framework used in bubble.js
    data_framework = '''{name: "%(name)s",
  text: [%(text)s],
  marker: {
    sizemode: "area",
    sizeref: 10,
    size : [%(size)s]
  },
  mode: "markers",
  y: [%(y)s],
  x: [%(x)s],
}'''
    
    sub_element = []    
    append_data = ''

    '''
         (x_axis, y_axis, bubble_axis)

         0: 'Non-negative Rate', \
         1: 'Number of Tweets', \
         2: 'Average Income per Person', \
         3: 'Average Income per Household', \
         4: 'Number of Households'
    '''
    
    # Process the data to be shown in Bubble Chart
    for city in L_lang:
        # Dictionary used to append 
        append_dict = {'name': '', 'text': '', 'size': '', 'y': '', 'x': ''}
        # Dictionary to store the data for every type of bubble
        dict_bubble_type = {0:'', 1:'', 2:'', 3:'', 4:'', 5:''}
        sub_element.append(data_framework)
        append_dict['name'] = city
        for ele in L_city:
            if ele not in dict_non_neg:
                print(ele, 'not in dict')
                continue
            append_dict['text'] = \
                append_dict['text']+ '''"''' + ele + '''",'''
            
            # Generate the data for every bubble type
            dict_bubble_type[0] = str(dict_non_neg[ele]) + ","
                
            dict_bubble_type[1] = str(dict_num_tweets[ele]) + ","

            if (mode == 'city'):
                dict_bubble_type[2] = str(dict_avg_income_pp[ele]) + ","
            
                dict_bubble_type[3] = str(dict_avg_income_ph[ele]) + ","
            
                dict_bubble_type[4] = str(dict_num_household[ele]) + ","
            
        append_dict['x'] = dict_bubble_type[x_axis]
        append_dict['y'] = dict_bubble_type[y_axis]
        append_dict['size'] = dict_bubble_type[bubble_axis]
        
        # Apply x y bubble axis value
        append_dict['text'] = append_dict['text'][0:-1]
        append_dict['size'] = append_dict['size'][0:-1]
        append_dict['y'] = append_dict['y'][0:-1]
        append_dict['x'] = append_dict['x'][0:-1]
        
        append_data += data_framework % append_dict
        append_data += ", "
        
    append_data = append_data[0:-2]
    
    # Update the bubble.js by over-writing the generated data
    bubble_js_file = open("js/generated/bubble.js", 'w')
    bubble_js_file.write(js_framework % (append_data, dict_axis[x_axis], \
                         dict_axis[y_axis]))
    bubble_js_file.close()
    
    global bubble_js
    bubble_js = js_framework % (append_data, dict_axis[x_axis], \
                         dict_axis[y_axis])


def html_column_generator():
    '''
    This function is to generate the column in the HTML form
    The column name are from the first row of the CSV file
    The HTML form is stored in html_column, which is directed inserted into
        the HTML file
    '''
    global html_column, dict_ref
    
    column_element = '''\n\t\t<option value="%s">%s</option>'''
    data_col = ''
    data_bins = ''
    for i in range(0, len(dict_ref)):
        data_col += column_element % (str(i), dict_ref[i][0])
        data_bins += column_element % (str(i), dict_ref[i][0] + ' (Bins)')
    
    html_column['filter_column'] = data_col
    html_column['agg_data'] = data_col
    
    html_column['data_column'] = data_bins
    html_column['data_row'] = data_bins


# Root of the webpage, refirect to index.html
@app.route('/', methods=['POST', 'GET'])
def index():
    global index_html
    return index_html

# start.html, request user's selected data
@app.route('/home', methods=['POST', 'GET'])
def home():
    global home_html
    connect_db()
    time.sleep(1)
    
    return home_html

# Data Explorer, to generate the data to be shown
@app.route('/data_exp', methods=['POST', 'GET'])
def data_exp():
    global dict_LCS, L_city, L_lang

    data_table = ''
    data_table += \
    '''<table class="table table-hover">
    <thead>
      <tr>\n'''
    data_table = data_table + "        <th></th>\n"
    
    # Make table head: city
    for city in L_city + ['Total']:
        data_table = data_table + "        <th>" + str(city).title() + "</th>\n"
    
    data_table += "      </tr>\n"
    data_table += "    </thead>\n"
    data_table += "    <tbody>\n"
    

    # Append the data into table
    for lang in L_lang + ['Total']:
        data_table += "      <tr>\n"
        data_table += "        <th>" + str(lang) + "</th>\n"
        for city in L_city + ['Total']:
            if lang == 'Total' or city == 'Total':
                table_ind = 'th'
            else:
                table_ind = 'td'
            data = dict_LCS[lang][city]
            data_table = data_table + "        <%s>" % table_ind + \
                         'Pos: %d<p>Neg: %d' %\
                         (data['pos'], data['neg'])\
                         + "</%s>\n" % table_ind
        data_table += "      </tr>\n"
    
    data_table += "    </tbody>\n"
    data_table += "</table>\n"
    
    # Print the HTML table in the terminal to check
    print(data_table)
    
    return data_exp_html.format(table__ = data_table)

# Bubble Chart Generator, generate and output the chart to js file
@app.route('/bubble', methods=['POST', 'GET'])
def bubble():
    global bubble_html, bubble_js
    global dict_axis
    
    # Analyze the data used to be output in bubble chart
    bubble_data_analyzer()
    # Output the default bubble chart
    bubble_js_generator('city', 0, 3, 2)
    '''
                 (x_axis, y_axis, bubble_axis)
    
                 0: 'Non-negative Rate', \
                 1: 'Number of Tweets', \
                 2: 'Average Income per Person', \
                 3: 'Average Income per Household', \
                 4: 'Number of Households'
    '''
    
    return bubble_html.replace('"0"', '"0" selected').replace('"13"', \
    '"13" selected').replace('"22"', '"22" selected').replace('(bubble__)',\
    '############').replace('(js__)', bubble_js)\
    .replace('s10"', 's10" selected')


# Bubble Chart Generator, when settings are changed
@app.route('/opt_bubble', methods=['POST', 'GET'])
def opt_bubble():
    global bubble_html, bubble_js
    global dict_axis
    
    # Get x, y, bubble axis meanings
    x = int(request.form['x'])
    y = int(request.form['y']) - 10
    bubble = int(request.form['z']) - 20
    size_ref = int(str(request.form['size'])[1:])
    print(size_ref)
                 
    # Analyze the data used to be output in bubble chart
    bubble_data_analyzer()
    # Output the default bubble chart
    bubble_js_generator(x, y, bubble)
    '''
                 (x_axis, y_axis, bubble_axis)
    
                 0: 'Non-negative Rate', \
                 1: 'Number of Tweets', \
                 2: 'Average Income per Person', \
                 3: 'Average Income per Household', \
                 4: 'Number of Households'
    '''
    
    # Output the Bubble Chart
    return bubble_html.replace('"' + str(x) + '"', '"'+str(x)+'" selected')\
                      .replace('1' + str(y) + '"', '1'+str(y)+'" selected')\
                      .replace('2' + str(bubble) + '"', \
                      '2' + str(bubble) + '" selected')\
                      .replace('(bubble__)', dict_axis[bubble])\
                      .replace('s' + str(size_ref) + '"',
                      's' + str(size_ref) + '" selected')\
                      .replace('(js__)', bubble_js)\
                      .replace('sizeref: 10', 'sizeref: ' + str(size_ref))


def generate_map_html(lang):
    global map_view_html
    global DB_URL
    global dict_LCS, L_city, L_lang

    STAT_URL = DB_URL + 'aurin_db/city_coord'
    r = requests.get(STAT_URL)
    d = r.json()['center']

    btn_txt = '''<a role="button" class="btn btn-primary" href="%s">%s</a>'''
    str_txt = ''

    for l in L_lang:
        str_txt += btn_txt % (l, l)
    
    data_table = {}
    for city in d:
        tweets = dict_LCS[lang][city]['pos'] + dict_LCS[lang][city]['neg']
        if tweets == 0:
            tweets = 1
        neg_percent = int(100.0 * dict_LCS[lang][city]['neg'] / tweets)
        neg_percent = min(100, neg_percent * 3)
        
        r = 0
        g = 0
        b = 0
        if neg_percent < 50:
            r = 5.1 * neg_percent
            g = 255
        else:
            r = 255
            g = 255 - 5.1*(neg_percent - 50)
            
        str_color = (hex(int(r))+'0')[2:4].upper()
        str_color += (hex(int(g))+'0')[2:4].upper()
        str_color += (hex(int(b))+'0')[2:4].upper()
        data_table[city.replace(' ', '', 10).lower()] = \
            {'center': d[city], 'population': tweets, 'fillColor': '*~#'+str_color+'*~'}

    ref_size = 300000 / math.sqrt(data_table['melbourne']['population'])
                        

    data_table = json.dumps(data_table).replace("'", '', 1000).\
                 replace('"', '', 1000).replace('*~', "'", 1000)
    print(data_table)
    
    return map_view_html.replace('{table__}', data_table).\
           replace('{size__}', str(ref_size)).\
           replace('{buttons__}', str_txt)

@app.route('/map_view/overview', methods=['POST', 'GET'])
def map_view():
    return generate_map_html('Total')

@app.route('/map_view/<lang>', methods=['POST', 'GET'])
def opt_map_view(lang):
    print('Language detected:', lang)
    return generate_map_html(lang)

# Flask main process
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5985, debug=True)
