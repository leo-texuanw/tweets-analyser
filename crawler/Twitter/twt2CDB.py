import sys
import tweepy
import time
import re
import pycouchdb

s_str = sys.argv[1]
inum = sys.argv[2]
itv = sys.argv[3]
auth_index = int(sys.argv[4])

s = pycouchdb.Server("http://cluster:cluster12@115.146.95.198:5984/",authmethod = "basic")

db_name = str(s_str + "_RES").replace("+","p")
db_name = db_name.replace("#","s")

try:
    rmt_db = s.database(db_name.lower())
except:
    print "no such DB remotely..creating DB " + db_name.lower()
    rmt_db = s.create(db_name.lower())

auth_index = 0
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

name_list = []
i = 0
#fetch origin name list, based on keyword
print "FIND ORIGIN NAMES: "
while (i<int(inum)):        
    isFailed = True
    while isFailed:
        try:
            public_tweets = api.search(q = s_str, rpp = 95) # , geocode = "-37.814, 144.96332, 500km"
        except:
            print "Connection Issue.. Reconnecting"
            isFailed = True
        else:
            isFailed = False
    for item in public_tweets:
        nameExisted = False
        temp_name = str(item.user.screen_name)  #find screen_names that's tweets contain keyword

        for every_name in name_list:    #check name list if current one duplicated
            if temp_name == every_name:
                nameExisted = True
                break

        if not nameExisted: #eliminate duplicates
            #print str(item) + "\n"
            name_list.append(temp_name)
            fw_org_name = open(s_str + "_name.txt", "a")
            fw_org_name.write(str(temp_name) + "\n")
            fw_org_name.close()

            #extract every followers' timeline text
            time.sleep(int(itv))
            print "FIND TIMELINES"
            isFailed = True
            while isFailed:
                try:
                    temp_msg = api.user_timeline(screen_name=temp_name, count=10)#get flw's timeline text
                except:
                    print "Connection Issue.. Reconnecting"
                    isFailed = True
                else:
                    isFailed = False

            item = temp_msg[0]
            temp_str = str(item)
            temp_cdnt = ptrn_cdnt.findall(temp_str)
            temp_lang = ptrn_lang.findall(temp_str)
            temp_flwcnt = ptrn_flwcnt.findall(temp_str)
            temp_id = ptrn_id.findall(temp_str)
            temp_sttscnt = ptrn_sttscnt.findall(temp_str)
            temp_tmz = ptrn_tmz.findall(temp_str)
            temp_dt = ptrn_dt.findall(temp_str)



            if not (len(temp_cdnt) == 0):
                print "TRUE"
                temp_cdnt = temp_cdnt[0]
            else:
                print "FALSE"
                temp_cdnt = "null"

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
            #write to local file
            wLine = "{\"name\":\"" + temp_name.strip() + "\",\"id\":\"" + temp_id + "\",\"status counts\":\"" + temp_sttscnt + "\",\"time zone\":\"" + temp_tmz + "\",\"datetime\":\"" + temp_dt + "\",\"msg\":\"" + str(item.text.encode("utf-8")).replace("\n"," ") + "\",\"cdnt\":\"" + str(temp_cdnt) + "}\n"
            fw_flw_twt = open (s_str + "_RES.txt", "a")
            fw_flw_twt.write(wLine)
            fw_flw_twt.close()
            try:
                rmt_db.save(dict(_id = temp_id, info = wLine))
            except:
                continue

    print "Proc: " + str(i*1.0/int(inum)*100) + "%"
    i += 1
    time.sleep (int(itv))