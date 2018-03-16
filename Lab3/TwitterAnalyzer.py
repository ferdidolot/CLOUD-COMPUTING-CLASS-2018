import json
import re
import operator
import json
from collections import Counter
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords") # download the stopword corpus on our computer
import string

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens


punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT']


#with open('ArtificialIntelligenceTweets.json', 'r') as f:
  #  for line in f:
      #  tweet = json.loads(line)
      #  tokens = preprocess(tweet['text'])
      #  print(tokens)



fname = 'ArtificialIntelligenceTweets.json'
with open(fname, 'r') as f:
    count_all = Counter()
    count_hashtag=Counter()
    count_only = Counter()

    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_stop = [term for term in preprocess(tweet['text']) if term not in stop]
        count_all.update(terms_stop)
        # Create a list with hashtags
        terms_hash = [term for term in preprocess(tweet['text'])
                      if term.startswith('#')]
        count_hashtag.update(terms_hash)
        #Create a list of terms onlyt skipping hashtags and mentions
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]
        count_only.update(terms_only)
    print ('Print the 10 top tokens')
    for word, index in count_all.most_common(10):
        print ('%s : %s' % (word, index))
    print ('Print the 10 top hashtags')
    for word, index in count_hashtag.most_common(10):
        print ('%s : %s' % (word, index))
    print ('Print the 10 top terms skipping mentions and hashtag')
    for word, index in count_only.most_common(10):
        print ('%s : %s' % (word, index))


