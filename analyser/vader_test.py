import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer


test_pos_tweets=[]
test_neg_tweets=[]

with open('./twitter/twitter-test-pos.txt','r',encoding='utf-8') as f:
    for line in f:
        test_pos_tweets.append(line.strip('\n'))
f.close()

with open('./twitter/twitter-test-neg.txt','r',encoding='utf-8') as f:
    for line in f:
        test_neg_tweets.append(line.strip('\n'))
f.close()

# Training data test as well
with open('./twitter/twitter-train-pos.txt','r',encoding='utf-8') as f:
    for line in f:
        test_pos_tweets.append(line.strip('\n'))
f.close()

with open('./twitter/twitter-train-neg.txt','r',encoding='utf-8') as f:
    for line in f:
        test_neg_tweets.append(line.strip('\n'))
f.close()


sid = SentimentIntensityAnalyzer()


'''
THRESHOLD = 0.3
Positive:  Accuracy = 50.8961% (229034/450003)
Negative:  Accuracy = 77.1266% (347073/450004)

THRESHOLD = 0.2
Positive:  Accuracy = 54.7152% (246220/450003)
Negative:  Accuracy = 73.0711% (328823/450004)

THRESHOLD = 0.1
Positive:  Accuracy = 55.8598% (251371/450003)
Negative:  Accuracy = 70.9425% (319244/450004)
'''
THRESHOLD = 0.1

correct_pos = 0
total_pos = 0
for sentence in test_pos_tweets:
     ss = sid.polarity_scores(sentence)
     correct_pos += 1 if ss['compound'] >= THRESHOLD else 0
     total_pos += 1

print('Positive:  Accuracy = %.4f%% (%d/%d)' % \
      (100.0*correct_pos/total_pos, correct_pos, total_pos))

correct_neg = 0
total_neg = 0
for sentence in test_neg_tweets:
     ss = sid.polarity_scores(sentence)
     correct_neg += 1 if ss['compound'] < THRESHOLD else 0
     total_neg += 1

print('Negative:  Accuracy = %.4f%% (%d/%d)' % \
      (100.0*correct_neg/total_neg, correct_neg, total_neg))
