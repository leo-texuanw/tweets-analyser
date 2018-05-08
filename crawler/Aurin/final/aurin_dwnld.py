import ConfigParser
import urllib2
import time
import re
import sys
import pycouchdb

search_keywds = sys.argv

config = ConfigParser.RawConfigParser()
config.read('openapi.cfg')

username=config.get('Auth', 'username')
password=config.get('Auth', 'password')

srch_lat_min = -38.1
srch_lat_max = -38
srch_lg_min = 144.7
srch_lg_max = 144.9
srch_area = (srch_lat_max - srch_lat_min) * (srch_lg_max - srch_lg_min)

bbox_info = "&bbox=" + str(srch_lat_min) + "," + str(srch_lg_min) + "," + str(srch_lat_max) + "," + str(srch_lg_max)
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
    retry = True
    while retry:
        url="http://openapi.aurin.org.au/wfs?service=WFS&version=1.1.0&request=GetCapabilities&outputFormat=json"
        try:
            raw_GetCpblt = aurin(url)
        except:
            print "Retrying"
            retry = True
        else:
            retry = False
    ptrn_name = re.compile(r"<Name>aurin:([^<>]+)<\/Name>")
    datasets = ptrn_name.findall(raw_GetCpblt)
    valid_datasets = []
    for item in datasets:
        isValid = True
        for i in range(1, len(search_keywds)):
            if not (item.find(search_keywds[i]) == -1):
                isValid = True
            else:
                isValid = False
                break
        if isValid:
            valid_datasets.append(item)
    print "THERE ARE TOTAL " + str(len(datasets)) + " DATASETS EXISTED.."
    print "valid_datasets number: " + str(len(valid_datasets))
    print "results:"
    for item in valid_datasets:
        print item

    ptrn_a_v = re.compile(r"\"([a-z_0-9]+)\":([0-9]+),")
    ptrn_bbox = re.compile(r",\"bbox\":\[([+-]?[0-9]+\.[0-9]+),([+-]?[0-9]+\.[0-9]+),([+-]?[0-9]+\.[0-9]+),([+-]?[0-9]+\.[0-9]+)\]}}]")
    maxFeatureNum = 5
    fw = open("RES.json","w")
    for i in range(0, len(valid_datasets) - 1):
        dataset = valid_datasets[i]
        url = "http://openapi.aurin.org.au/wfs?request=GetFeature&service=WFS&version=1.1.0&TypeName=" + dataset + "&MaxFeatures=" + str(maxFeatureNum) + bbox_info + "&outputFormat=Application/json"
        retry = True
        while retry:    #when occuring connection issue, just retry it
            try:
                raw_GetFeature = aurin(url)
            except:
                retry = True
                print "Connection Exception..Retrying"
            else:
                retry = False   #get out of while loop
        isValid = False
        wLine_data = ""

        bbox_w = ptrn_bbox.findall(str(raw_GetFeature))
        valid_ratio = 0.0
        if len(bbox_w) > 0:
            (lg_min, lat_min, lg_max, lat_max) = bbox_w[0]
            box_area = (float(lg_max) - float(lg_min)) * (float(lat_max) - float(lat_min))
            valid_ratio = srch_area / box_area
            isValid = True

        if isValid:
            for item in ptrn_a_v.findall(str(raw_GetFeature)):
                (a_name, a_value) = item
                tmp_av = "\"" + a_name + "\":\"" + str(round(float(a_value)*valid_ratio)) + "\""
                wLine_data += ("," + tmp_av)

        if not (wLine_data == ""):
            isValid = True
        else:
            isValid = False

        if isValid:
            wLine = "{\"dataset\":\"" + dataset + "\"" + wLine_data + ",\"ratio\":\"" + str(valid_ratio) + "\"}\n"
            fw.write(wLine)
    fw.close()