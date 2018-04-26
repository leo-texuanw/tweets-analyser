import sys
import tweepy
import time

s_str = sys.argv[1]
inum = sys.argv[2]
itv = sys.argv[3]
print "Search String: " + s_str
print "Search Times: " + inum
print "Search Interval: " + itv

consumer_key = "4WoQyZGgiD4rZliV7Jlgru7x3"
consumer_secret = "X6wFOrlCV6GwuQTSZCOMah5nrnSOUsGLzNdG7BpU8l52j6LQSH"
access_token = "989116503399190534-Ly0vzI3MrNXVrxDYkzuYi6BfoRGTn8I"
access_token_secret = "KpBOmRW12CnHLROnE46fuFDmMuuCC2UX63P6NdwwGvmud"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)



i = 0
while (i<int(inum)):	
	ft = open (s_str + ".txt", "a")
	public_tweets = api.search(q = s_str, rpp = 95, since_id = i*100)
	for item in public_tweets:
		ft.write("# USERNAME #" + str(item.user.screen_name.encode('utf-8')) + "# USERTEXT #" + str(item.text.encode('utf-8')) + "\n")
	print i
	i+=1
	ft.close()
	time.sleep (int(itv))