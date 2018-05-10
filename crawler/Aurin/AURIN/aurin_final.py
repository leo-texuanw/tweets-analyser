import ConfigParser
import urllib2
import time
import re
import sys
import pycouchdb

argv_in = sys.argv

db_usr = sys.argv[1]
db_pwd = sys.argv[2]
db_ip = sys.argv[3]
db_port = sys.argv[4]
ex_db_info = "http://" + db_usr + ":" + db_pwd + "@" + db_ip + ":" + db_port + "/"

keywds = []
for i in range(5, len(argv_in)):
    keywds.append(argv_in[i].strip())

try:
    s = pycouchdb.Server(ex_db_info, authmethod = "basic")
except:
    print "unable connecting to DB"
    sys.exit(0)

db_name = "aurin_db"

try:
    rmt_db = s.database(db_name.lower())
except:
    print "no such DB remotely..creating DB " + db_name.lower()
    rmt_db = s.create(db_name.lower())

config = ConfigParser.RawConfigParser()
config.read('openapi.cfg')

username=config.get('Auth', 'username')
password=config.get('Auth', 'password')

fr_ct = open("CitiesGrid.txt", "r")
ct_lines = fr_ct.readlines()
fr_ct.close()
ct_infos = []
for item in ct_lines:
    substr = item.split(";")
    if substr[0].strip() == "+":
        temp_ct_name = substr[1].strip()
        temp_lat = substr[2].strip()
        temp_lg = substr[3].strip()
        temp_offset = substr[4].strip()
        temp_lat_min = float(temp_lat) - float(temp_offset)
        temp_lat_max = float(temp_lat) + float(temp_offset)
        temp_lg_min = float(temp_lg) - float(temp_offset)
        temp_lg_max = float(temp_lg) + float(temp_offset)
        temp_area = float(temp_offset)*float(temp_offset)
        temp_bbox = "&bbox=" + str(temp_lat_min) + "," + str(temp_lg_min) + "," + str(temp_lat_max) + "," + str(temp_lg_max)
        ct_infos.append( (temp_ct_name, temp_bbox, temp_area) )

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
        for kw in keywds:
            if not (item.find(kw) == -1):
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


    for ct_info in ct_infos:
        (temp_ct_name, temp_bbox, temp_area) = ct_info
        print "Retrieving data for: " + temp_ct_name
        db_id = 0
        for dataset in valid_datasets:
            url = "http://openapi.aurin.org.au/wfs?request=GetFeature&service=WFS&version=1.1.0&TypeName=" + dataset + "&MaxFeatures=" + str(maxFeatureNum) + temp_bbox + "&outputFormat=Application/json"
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

            bbox_aurin = ptrn_bbox.findall(str(raw_GetFeature))
            valid_ratio = 0.0

            if len(bbox_aurin) > 0:
                (lg_min, lat_min, lg_max, lat_max) = bbox_aurin[0]
                box_area = (float(lg_max) - float(lg_min)) * (float(lat_max) - float(lat_min))
                valid_ratio = float(temp_area) / box_area
                isValid = True

            if isValid:
                for item in ptrn_a_v.findall(str(raw_GetFeature)):
                    (a_name, a_value) = item
                    tmp_av = a_name + ":" + str(round(float(a_value)*valid_ratio))
                    wLine_data += (tmp_av + ",")           

            if not (wLine_data == ""):
                isValid = True
            else:
                isValid = False

            if isValid:
                dict_main = {"city_name" : temp_ct_name, "search_bbox" : temp_bbox.split("=")[1], "block_bbox" : str(bbox_aurin[0]), "scale_ratio" : str(valid_ratio), "dataset_name" : dataset}
                dict_data = {}
                dict_kws = {}
                kw_cnt = 0

                for item in keywds:
                    dict_kws["KW" + str(kw_cnt)] = item

                for item in ptrn_a_v.findall(str(raw_GetFeature)):
                    (a_name, a_value) = item
                    dict_data[a_name] = a_value

                dict_main["data"] = dict_data
                dict_main["keywords"] = dict_kws

                rmt_db.save(dict_main)
                db_id += 1
                print db_id
        