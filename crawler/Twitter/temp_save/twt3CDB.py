import sys
import tweepy
import time
import re
import pycouchdb

def subproc (in_s_str, in_auth_index):
    #s_str = sys.argv[1]
    #itv = sys.argv[2]
    #auth_index = int(sys.argv[3])
    s_str = str(in_s_str)
    auth_index = int(in_auth_index)

    print s_str + "\n\n"

    geo_cityname = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "GoldCoast", "Canberra", "Newcastle", "Wollongong", "LoganCity"]
    geo_lat = [-33.868, -37.814, -27.468, -31.952, -34.929, -28, -35.283, -32.927, -34.424, -27.639]
    geo_long = [151.207, 144.963, 153.028, 115.861, 138.599, 153.431, 149.128, 151.776, 150.893, 153.109]

    s = pycouchdb.Server("http://cluster:cluster12@115.146.95.198:5985/",authmethod = "basic")

    db_name = str(s_str + "_RES").replace("+","p")
    db_name = db_name.replace("#","s")

    try:
        rmt_db = s.database(db_name.lower())
    except:
        print "no such DB remotely..creating DB " + db_name.lower()
        rmt_db = s.create(db_name.lower())

    consumer_key = ["4WoQyZGgiD4rZliV7Jlgru7x3","GiOfCoiBPM2GfkHkyk0xP2Gxg","KBTRSq44s8Ri3KOGVhhcVRqwb"]
    consumer_secret = ["X6wFOrlCV6GwuQTSZCOMah5nrnSOUsGLzNdG7BpU8l52j6LQSH","VdtLvIXOwkpUK0cIpELvkoBlke237NijKSV9HraBlO1jXBMvAO","LCjfqzDkU6ETIAjJRBkgsC60tQwSGdLXM5xfYV95nG0rwk6WE8"]
    access_token = ["989116503399190534-Ly0vzI3MrNXVrxDYkzuYi6BfoRGTn8I","989116503399190534-j5WwbrEBCRsZonsVxcJ2G9rHN45egfZ","989116503399190534-jeuPqHxaWLRhB6T7vc7skaTjiXzoYI6"]
    access_token_secret = ["KpBOmRW12CnHLROnE46fuFDmMuuCC2UX63P6NdwwGvmud","r5woA2pcB51cTsJckVAQV1z6gwvTH3nE6T9MOQTgL3wil","qj6E0EIWvhcR2kEIvveWVkqq8XM9cd27U9iqE7xbr1fCf"]

    auth = tweepy.OAuthHandler(consumer_key[auth_index], consumer_secret[auth_index])
    auth.set_access_token(access_token[auth_index], access_token_secret[auth_index])
    api = tweepy.API(auth,wait_on_rate_limit=True)

    ptrn_cdnt = re.compile(r"coordinates=\[\[\[(-?[0-9]+\.[0-9]+), (-?[0-9]+\.[0-9]+)\], \[-?[0-9]+\.[0-9]+, -?[0-9]+\.[0-9]+\], \[(-?[0-9]+\.[0-9]+), (-?[0-9]+\.[0-9]+)\], \[-?[0-9]+\.[0-9]+, -?[0-9]+\.[0-9]+\]\]\]")   #coordinate
    ptrn_flwcnt = re.compile(r"followers_count=([0-9]+)")   #follower counts
    ptrn_id = re.compile(r"id_str=u\'([0-9]+)\'")   #usr_id
    ptrn_sttscnt = re.compile(r"statuses_count=([0-9]+)")   #status counts  
    ptrn_lang = re.compile(r"lang=u\'([a-zA-Z]+)\'")    #language
    ptrn_tmz = re.compile(r"time_zone=u\'([a-zA-Z]+)\'")    #timezone
    ptrn_dt = re.compile(r"datetime\.datetime\(([0-9, ]+)\)")   #datetime

    #name_list = []

    for geo_index in range(len(geo_cityname)):

        s_radius = 8
        offset = 0.3
        inc = 0.1
        temp_long = geo_long[geo_index]
        temp_lat = geo_lat[geo_index]
        current_long = temp_long - offset
        max_long = temp_long + offset
        current_lat = temp_lat - offset
        max_lat = temp_lat + offset

        avail_cnt = 0
        name_list = []

        while current_lat <= max_lat:
            while current_long <= max_long:
                # for the current GPS info
                temp_geocode = str(current_lat) + "," + str(current_long) + "," + str(s_radius) + "km" # no space allowed
                #fetch origin name list, based on keyword
                #name_list = []
                print "FIND ORIGIN NAMES in " + geo_cityname[geo_index] + " @ lat: " + str(current_lat) + " long: " + str(current_long)
                
                # applying for retrieving data
                isFailed = True
                while isFailed:
                    try:
                        #public_tweets = api.search(q = s_str, lang = "en", count = 150, geocode = temp_geocode)
                        time.sleep (int(5))
                        public_tweets = tweepy.Cursor(api.search, q = s_str, lang = "en", result_type = "recent", geocode = temp_geocode).items()
                    except:
                        print "Connection Issue.. Reconnecting"
                        isFailed = True
                    else:
                        isFailed = False

                
                for item in public_tweets:
                    nameExisted = False
                    temp_name = str(item.user.screen_name) + str(item.text.encode("utf-8")).replace("\n"," ")  #find screen_names that's tweets contain keyword

                    for every_name in name_list:    #check name list if current one duplicated
                        if temp_name == every_name:
                            nameExisted = True
                            #print "SAME NAME"
                            break

                    if not nameExisted: #eliminate duplicates name
                        avail_cnt += 1
                        name_list.append(temp_name)
                        #fw_org_name = open(s_str + "_name.txt", "a")
                        #fw_org_name.write(str(temp_name) + "\n")
                        #fw_org_name.close()

                        temp_str = str(item)
                        temp_cdnt = ptrn_cdnt.findall(temp_str)
                        temp_lang = ptrn_lang.findall(temp_str)
                        temp_flwcnt = ptrn_flwcnt.findall(temp_str)
                        temp_id = ptrn_id.findall(temp_str)
                        temp_sttscnt = ptrn_sttscnt.findall(temp_str)
                        temp_tmz = ptrn_tmz.findall(temp_str)
                        temp_dt = ptrn_dt.findall(temp_str)

                        if not (len(temp_cdnt) == 0):
                            #print "TRUE"
                            temp_cdnt = temp_cdnt[0]
                        else:
                            #print "FALSE"
                            temp_cdnt = str(current_lat) + "," + str(current_long) + "," + str(s_radius) + "km"

                        if not (len(temp_lang) == 0):
                            temp_lang = temp_lang[0]
                        else:
                            temp_lang = "null"

                        if not (len(temp_flwcnt) == 0):
                            temp_flwcnt = temp_flwcnt[0]
                        else:
                            temp_flwcnt = "null"

                        if not (len(temp_id) == 0):
                            temp_id = temp_id[0]
                        else:
                            temp_id = "null"

                        if not (len(temp_sttscnt) == 0):
                            temp_sttscnt = temp_sttscnt[0]
                        else:
                            temp_sttscnt = "null"

                        if not (len(temp_tmz) == 0):
                            temp_tmz = temp_tmz[0]
                        else:
                            temp_tmz = "null" 

                        if not (len(temp_dt) == 0):
                            temp_dt = temp_dt[0]
                        else:
                            temp_dt = "null"
                        temp_msg = str(item.text.encode("utf-8")).replace("\n"," ")
                        #write to local file
                        wLine = "{\"name\":\"" + str(item.user.screen_name).strip() + "\",\"id\":\"" + temp_id + "\",\"status counts\":\"" + temp_sttscnt + "\",\"location filter\":\"" + geo_cityname[geo_index] + "\",\"time zone\":\"" + temp_tmz + "\",\"datetime\":\"" + temp_dt + "\",\"msg\":\"" + temp_msg + "\",\"cdnt\":\"" + str(temp_cdnt) + "\"}\n"
                        fw_flw_twt = open (s_str + "_RES.txt", "a")
                        fw_flw_twt.write(wLine)
                        fw_flw_twt.close()
                        try:
                            rmt_db.save(dict(_id = str(hash(temp_id + temp_msg)), info = wLine))
                        except:
                            continue
                    else:
                        continue
                print  "TOTAL COUNTS: " + str(avail_cnt)
                current_long += inc

            current_lat += inc
            current_long = temp_long - offset