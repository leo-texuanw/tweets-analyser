import sys
import tweepy
import time

file_name = sys.argv[1]
itv = sys.argv[2]
print ("file name: " + file_name)
print ("Loop Interval: " + itv)

consumer_key = "KBTRSq44s8Ri3KOGVhhcVRqwb"
consumer_secret = "LCjfqzDkU6ETIAjJRBkgsC60tQwSGdLXM5xfYV95nG0rwk6WE8"
access_token = "989116503399190534-jeuPqHxaWLRhB6T7vc7skaTjiXzoYI6"
access_token_secret = "qj6E0EIWvhcR2kEIvveWVkqq8XM9cd27U9iqE7xbr1fCf"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
print ("Login Success")

fr = open (file_name + ".txt", "r")
rlines = fr.readlines()
fr.close()

print ("Read Success")

for follower_name in rlines:
    temp_msg = api.user_timeline(follower_name.strip())
    for item in str(temp_msg):
        fw = open (file_name + "_MSG.txt", "a")
        fw.write(str(item) + "\n")
        fw.close()
    print(str("twt_name_follower_msg"))
    time.sleep(int(itv))