import sys
import tweepy
import time

s_str = sys.argv[1]
inum = sys.argv[2]
itv = sys.argv[3]
print ("Search String: " + s_str)
print ("Search Times: " + inum)
print ("Search Interval: " + itv)

consumer_key = "4WoQyZGgiD4rZliV7Jlgru7x3"
consumer_secret = "X6wFOrlCV6GwuQTSZCOMah5nrnSOUsGLzNdG7BpU8l52j6LQSH"
access_token = "989116503399190534-Ly0vzI3MrNXVrxDYkzuYi6BfoRGTn8I"
access_token_secret = "KpBOmRW12CnHLROnE46fuFDmMuuCC2UX63P6NdwwGvmud"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth,wait_on_rate_limit=True)
name_list = []
i = 0
while (i<int(inum)):	
	
	public_tweets = api.search(q = s_str, rpp = 90)
	for item in public_tweets:
		nameExisted = False
		temp_name = str(item.user.screen_name)
		for every_name in name_list:
			if temp_name == every_name:
				nameExisted = True
				break
		if not nameExisted:
			name_list.append(temp_name)
			ft = open (s_str + "_name.txt", "a")
			ft.write(str(temp_name) + "\n")
			ft.close()
	print (str("twt_name"))
	print (len(name_list))
	i += 1
	time.sleep (int(itv))