import ConfigParser
import urllib2
import time
import re
import sys

search_str = sys.argv[1]

config = ConfigParser.RawConfigParser()
config.read('openapi.cfg')

username=config.get('Auth', 'username')
password=config.get('Auth', 'password')
#Latitude from -43.00311 to -12.46113 and longitude from 113.6594 to 153.61194.
#aus#bbox_info ="-43.00311,113.6594,-12.46113,153.61194"
#bbox_info = "bbox=-38.1,144.7,-37.5,145.5"
bbox_info = "bbox=-38.1,144.7,-38,145"
# Submit an authenticated request to the AURIN Open API
def aurin(url):

    # create an authenticated HTTP handler and submit URL
    password_manager = urllib2.HTTPPasswordMgrWithDefaultRealm()
    password_manager.add_password(None, url, username, password)
    auth_manager = urllib2.HTTPBasicAuthHandler(password_manager)
    opener = urllib2.build_opener(auth_manager)
    urllib2.install_opener(opener)
    req = urllib2.Request(url)
    handler = urllib2.urlopen(req)
    return handler.read()

if __name__ == "__main__":
#GET_CAPABILITIES
	url="http://openapi.aurin.org.au/wfs?service=WFS&version=1.1.0&request=GetCapabilities&outputFormat=json"
	raw_GetCpblt = aurin(url)

	ptrn_name = re.compile(r"<Name>aurin:([^<>]+)<\/Name>")
	datasets = ptrn_name.findall(raw_GetCpblt)
	##for item in dataset_names:
	##	print item
	print "THERE ARE TOTAL " + str(len(datasets)) + " DATASETS EXISTED.."

#find attributes' names for each dataset
	ptrn_name = re.compile(r"name=\"(.+)\" nillable")
	dataset_attribute = []
	cnt = 0
	size = len(datasets)
	for dataset in datasets:
	    url = 'http://openapi.aurin.org.au/wfs?request=DescribeFeatureType&service=WFS&version=1.1.0&typeName=' + dataset
	    retry = True
	    raw_DFT = ""
	    while retry:	#when occuring connection issue, just retry it
	        try:
	            raw_DFT = aurin(url)
	        except:
	            retry = True
	            print "Connection Exception..Retrying"
	        else:
	            retry = False   #get out of while loop
	    temp_names = ptrn_name.findall(raw_DFT)
	    dataset_attribute.append((dataset, temp_names)) #operate every attribute's name in one dataset
	    print "GET ATTRIBUTES: " + str(cnt*1.0/size*100) + "%"
	    cnt += 1

#trim datasets by keyword
srch_datasets = []
srch_keyword = search_str
for da in dataset_attribute:
    if not (str(da).find(srch_keyword) == -1):
        srch_datasets.append(da[0]) #record necessary datasets' names only

#get first X records for each trimmed dataset
	srch_res = []
	cnt = 0
	size = len(srch_datasets)
	for dataset in srch_datasets:
	    url = "http://openapi.aurin.org.au/wfs?request=GetFeature&service=WFS&version=1.1.0&TypeName=" + dataset + "&MaxFeatures=3&" + bbox_info + "&outputFormat=json"
	    retry = True
	    raw_GetFeature = ""
	    while retry:	#when occuring connection issue, just retry it
	        try:
	            raw_GetFeature = aurin(url)
	        except:
	            retry = True
	            print "Connection Exception..Retrying"
	        else:
	            retry = False   #get out of while loop
	    fw = open(srch_keyword + ".json","a")
	    fw.write(str(raw_GetFeature))
	    fw.close()
	    print "GET FEATURES: " + str(cnt*1.0/size*100) + "%"
	    cnt += 1