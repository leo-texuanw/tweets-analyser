import sys
import tweepy
import time
import re
import pycouchdb

def subproc (key_word, usr_op, rmt_db, auth_info, ct_infos):

    s_str = str(key_word)

    isWTL = False # write to local file
    for item in usr_op:
        if item[0] == "write_to_local":
            if item[1] == "True":
                isWTL = True
            else:
                isWTL = False

    consumer_key = auth_info[0]
    consumer_secret = auth_info[1]
    access_token = auth_info[2]
    access_token_secret = auth_info[3]

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth,wait_on_rate_limit=True)

    ptrn_cdnt = re.compile(r"coordinates=\[\[\[(-?[0-9]+\.[0-9]+), (-?[0-9]+\.[0-9]+)\], \[-?[0-9]+\.[0-9]+, -?[0-9]+\.[0-9]+\], \[(-?[0-9]+\.[0-9]+), (-?[0-9]+\.[0-9]+)\], \[-?[0-9]+\.[0-9]+, -?[0-9]+\.[0-9]+\]\]\]")   #coordinate
    ptrn_flwcnt = re.compile(r"followers_count=([0-9]+)")   #follower counts
    ptrn_id = re.compile(r"id_str=u\'([0-9]+)\'")   #usr_id
    ptrn_sttscnt = re.compile(r"statuses_count=([0-9]+)")   #status counts  
    ptrn_lang = re.compile(r"lang=u\'([a-zA-Z]+)\'")    #language
    ptrn_tmz = re.compile(r"time_zone=u\'([a-zA-Z]+)\'")    #timezone
    ptrn_dt = re.compile(r"datetime\.datetime\(([0-9, ]+)\)")   #datetime
    ptrn_rt = re.compile(r"retweeted=True")    #retweet

    for item in ct_infos:

        s_radius = 8
        offset = 0.4
        inc = 0.1
        (temp_ctname, temp_lat, temp_long) = item

        current_long = float(temp_long) - offset
        max_long = float(temp_long) + offset
        current_lat = float(temp_lat) - offset
        max_lat = float(temp_lat) + offset

        avail_cnt = 0
        name_list = []

        db_name = temp_ctname.replace(" ","_")

        while current_lat <= max_lat:
            while current_long <= max_long:
                # for the current GPS info
                temp_geocode = str(current_lat) + "," + str(current_long) + "," + str(s_radius) + "km" # no space allowed
                #fetch origin name list, based on keyword

                print "FIND ORIGIN NAMES in " + temp_ctname + " @ lat: " + str(current_lat) + " long: " + str(current_long)
                
                # applying for retrieving data
                isFailed = True
                while isFailed:
                    try:
                        time.sleep (10)
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
                            break

                    if not nameExisted: #eliminate duplicates name
                        avail_cnt += 1
                        name_list.append(temp_name)

                        temp_str = str(item)
                        temp_cdnt = ptrn_cdnt.findall(temp_str)
                        temp_lang = ptrn_lang.findall(temp_str)
                        temp_flwcnt = ptrn_flwcnt.findall(temp_str)
                        temp_id = ptrn_id.findall(temp_str)
                        temp_sttscnt = ptrn_sttscnt.findall(temp_str)
                        temp_tmz = ptrn_tmz.findall(temp_str)
                        temp_dt = ptrn_dt.findall(temp_str)
                        temp_rt = ptrn_rt.findall(temp_str)

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

                        if not (len(temp_rt) == 0):
                            temp_rt = "True"
                        else:
                            temp_rt = "False"

                        temp_msg = str(item.text.encode("utf-8")).replace("\n"," ")
                        wLine = "{\"name\":\"" + str(item.user.screen_name).strip() + "\",\"id\":\"" + temp_id + "\",\"status counts\":\"" + temp_sttscnt + "\",\"location filter\":\"" + temp_ctname + "\",\"time zone\":\"" + temp_tmz + "\",\"datetime\":\"" + temp_dt + "\",\"retweeted\":\"" + temp_rt + "\",\"keyword\":\"" + key_word + "\",\"msg\":\"" + temp_msg + "\",\"cdnt\":\"" + str(temp_cdnt) + "\"}\n"
                        
                        if isWTL:   #write to local file
                            fw_flw_twt = open (s_str + ".txt", "a")
                            fw_flw_twt.write(wLine)
                            fw_flw_twt.close()
                            
                        try:
                            rmt_db.save(dict(_id = str(hash(temp_id + temp_msg)), name = str(item.user.screen_name).strip(), usr_id = temp_id, status_count = temp_sttscnt, location = temp_ctname, time_zone = temp_tmz, datetime = temp_dt, retweeted = temp_rt, keyword = key_word, msg = temp_msg, coordinate = str(temp_cdnt)))
                        except:
                            continue
                    else:
                        continue
                #print  "TOTAL COUNTS: " + str(avail_cnt)
                current_long += inc

            current_lat += inc
            current_long = float(temp_long) - offset