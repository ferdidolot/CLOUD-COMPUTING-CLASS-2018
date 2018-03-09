import tweepy
import json
import configparser 
from nltk.tokenize import word_tokenize
import re
	
from tweepy import OAuthHandler

def ConfigSectionMap(section):
    dict1 = {}
    options = Config.options(section)
    for option in options:
        try:
            dict1[option] = Config.get(section, option)
            if dict1[option] == -1:
                DebugPrint("skip: %s" % option)
        except:
            print("exception on %s!" % option)
            dict1[option] = None
    return dict1

Config = configparser.ConfigParser()
Config.read("configuration.ini")
#print Config.sections()

consumer_key = ConfigSectionMap("TwitterAPI")['consumerkey']
consumer_secret = ConfigSectionMap("TwitterAPI")['consumersecret']
access_token = ConfigSectionMap("TwitterAPI")['accesstoken']
access_secret = ConfigSectionMap("TwitterAPI")['accesstokensecret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
  
api = tweepy.API(auth)

user = api.me()
 
tweet = 'RT @JordiTorresBCN: just an example! :D http://JordiTorres.Barcelona #masterMEI'
print ("Tweer preprocessing:")
print(word_tokenize(tweet))


#Capturing emotions, hashtag, URLs

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


tweet = 'RT @JordiTorresBCN: just an example! :D http://JordiTorres.Barcelona #masterMEI'
print ("Tweer preprocessing after capturing emotions, hashtag, URLs:")
print(preprocess(tweet))

