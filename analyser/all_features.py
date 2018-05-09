import nltk
import pickle

def get_word_features(tweets):
        all_words = []
        for (words, sentiment) in tweets:
          all_words.extend(words)
        wordlist = nltk.FreqDist(all_words)
        word_features = []
        for feature in wordlist:
            if wordlist[feature] > 5000:
                word_features.append(feature)
        print(len(word_features))
        return word_features

def extract_features(document):
        document_words = set(document)
        features = {}
        for word in word_features:
            features['contains(%s)' % word] = (word in document_words)
        return features


f = open('twitter_classifier.pickle', 'rb')
classifier = pickle.load(f)
f.close()

print("Model loaded")

train_pos_tweets=[]
train_neg_tweets=[]
test_pos_tweets=[]
test_neg_tweets=[]


with open('./twitter/twitter-train-pos.txt','r',encoding='utf-8') as f:
    for line in f:
        train_pos_tweets.append((line,'pos'))
f.close()

with open('./twitter/twitter-train-neg.txt','r',encoding='utf-8') as f:
    for line in f:
        train_neg_tweets.append((line,'neg'))
f.close()

with open('./twitter/twitter-test-pos.txt','r',encoding='utf-8') as f:
    for line in f:
        test_pos_tweets.append((line,'pos'))
f.close()

with open('./twitter/twitter-test-neg.txt','r',encoding='utf-8') as f:
    for line in f:
        test_neg_tweets.append((line,'neg'))
f.close()

train_tweets = []
test_tweets = []

for (words, sentiment) in train_pos_tweets + train_neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    train_tweets.append((words_filtered, sentiment))

for (words, sentiment) in test_pos_tweets + test_neg_tweets:
    words_filtered = [e.lower() for e in words.split() if len(e) >= 3]
    test_tweets.append((words_filtered, sentiment))

print("Tweets filtered")

word_features = get_word_features(train_tweets+test_tweets)
print("Word Features Generated")

