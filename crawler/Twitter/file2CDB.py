import pycouchdb
import sys
import re

file_name = sys.argv[1]
fr = open (file_name + ".txt", "r")
rLines = fr.readlines()
fr.close()

db_name = file_name.replace("+","p")
db_name = db_name.replace("#","s")
print db_name
ptrn_id = re.compile(r"\"id\":\"([0-9]+)\"")
#get instance of remote DB
s = pycouchdb.Server("http://cluster:cluster12@115.146.95.198:5984/",authmethod = "basic")
try:
	temp_db = s.create(db_name.lower())
except:
	temp_db = s.database(db_name.lower())
#temp_db = s.database("testdb1")
#doc = temp_db.get(id)
size = len(rLines)
cnt = 0
for rLine in rLines:
	temp_id = ptrn_id.findall(rLine)[0]
	try:
		temp_db.save(dict(_id = temp_id, info = rLine))
	except:
		size -= 1
		continue
	
	print "Progress: " + str(cnt*1.0/size*100) + "%"
	cnt += 1

	