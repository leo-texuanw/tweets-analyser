import nltk
from nltk.corpus import wordnet
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

mytext = "Hello Mr. Adam, how are you? I hope everything is going well. Today is a good day, see you dude." 
print(nltk.tokenize.sent_tokenize(mytext))

syn = nltk.corpus.wordnet.synsets("pain")
print(syn[0].definition())
print(syn[0].examples())
print()

synonyms = []
for syn in wordnet.synsets('friend'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
synonyms = [w.lower() for w in synonyms]
synonyms = list(set(synonyms))
print(sorted(synonyms))
print()

antonyms = []
for syn in wordnet.synsets("well"):
    for l in syn.lemmas():
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
antonyms = list(set(antonyms))
print(sorted(antonyms))
print()

stemmer = PorterStemmer() 
print(stemmer.stem('increases'))
print()

lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('increases'))
print(lemmatizer.lemmatize('playing', pos="v")) 
print(lemmatizer.lemmatize('playing', pos="n")) 
print(lemmatizer.lemmatize('playing', pos="a")) 
print(lemmatizer.lemmatize('playing', pos="r"))
