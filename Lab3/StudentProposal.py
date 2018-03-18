from collections import Counter
import json
import re
import nltk
from nltk.corpus import stopwords
nltk.download("stopwords")
import string

import matplotlib as mpl
mpl.rcParams['figure.figsize'] = (14,14)
import matplotlib.pyplot as plt

#print "backend: ", plt.get_backend()

#Switch backend is necessary to produce the plot
plt.switch_backend('agg')

#print "backend: ", plt.get_backend()

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['rt', 'via', 'RT']

# Capturing emotions, hashtag, URLs

emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>',  # HTML tags
    r'(?:@[\w_]+)',  # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)",  # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+',  # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)',  # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])",  # words with - and '
    r'(?:[\w_]+)',  # other words
    r'(?:\S)'  # anything else
]

tokens_re = re.compile(r'(' + '|'.join(regex_str) + ')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^' + emoticons_str + '$', re.VERBOSE | re.IGNORECASE)


def tokenize(s):
    return tokens_re.findall(s)


def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

fname = 'WeekendTweets.json'
with open(fname, 'r') as f:
    count_all = Counter()
    count_hashtag = Counter()
    count_only = Counter()
    count_men = Counter()

    for line in f:
        tweet = json.loads(line)
        # Create a list with all the terms
        terms_hash = [term for term in preprocess(tweet['text']) if term not in stop]
        count_all.update(terms_hash)

        # Create a list with hashtags
        terms_hash = [term for term in preprocess(tweet['text']) if term.startswith('#') and term not in stop]
        count_hashtag.update(terms_hash)

        #Create a list of terms onlyt skipping hashtags and mentions
        terms_only = [term for term in preprocess(tweet['text'])
                      if term not in stop and
                      not term.startswith(('#', '@'))]
        count_only.update(terms_only)

        # Create a list with mentions
        terms_men = [term for term in preprocess(tweet['text']) if term.startswith('@') and term not in stop]
        count_men.update(terms_men)



def generatePlot(count,plotName):

    print(count.most_common(15))
    sorted_x, sorted_y = zip(*count.most_common(15))
    print(sorted_x, sorted_y)

    plt.bar(range(len(sorted_x)), sorted_y, width=0.75, align='center')
    plt.xticks(range(len(sorted_x)), sorted_x, rotation=60)
    plt.axis('tight')
    plt.show()                  # show it on IDE
    plt.savefig(plotName)  # save it on a file
    plt.gcf().clear()           #forget the previous char




# Print and generate the plot for the first 15 most frequent tokens
generatePlot(count_all, 'StudentProposal_Tokens.png')

# Print and generate the plot for the first 15 most frequent hashtags
generatePlot(count_hashtag, 'StudentProposal_Hashtags.png')

# Print and generate the plot for the first 15 most frequent tokens skipping hashtags and mentions
generatePlot(count_only, 'StudentProposal_NoHashtagsMentions.png')

# Print and generate the plot for the first 15 most frequent mentions
generatePlot(count_men, 'StudentProposal_Mentions.png')