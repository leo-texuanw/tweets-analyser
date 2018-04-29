import sys
import tweepy
import time

file_name = sys.argv[1]
itv = sys.argv[2]
print ("file name: " + file_name)
print ("Loop Interval: " + itv)

consumer_key = "GiOfCoiBPM2GfkHkyk0xP2Gxg"
consumer_secret = "VdtLvIXOwkpUK0cIpELvkoBlke237NijKSV9HraBlO1jXBMvAO"
access_token = "989116503399190534-j5WwbrEBCRsZonsVxcJ2G9rHN45egfZ"
access_token_secret = "r5woA2pcB51cTsJckVAQV1z6gwvTH3nE6T9MOQTgL3wil"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)

isOpened = False
while (not isOpened):
	try:
		fr = open (file_name + ".txt", "r")
		isOpened = True
	except IOError:
		isOpened = False

rlines = fr.readlines()
fr.close()

print ("START")
for rline in rlines:
	follower_list = api.followers(id = rline.strip())
	fw = open (file_name + "_follower.txt", "a")
	for item in follower_list:
		fw.write(str(item.screen_name) + "\n")
	fw.close()
	print (str("twt_name_follower"))
	time.sleep(int(itv))


	