import tweepy
import json
import configparser 
	
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
 
for status in tweepy.Cursor(api.home_timeline).items(1):
    print(json.dumps(status._json, indent=2))

for friend in tweepy.Cursor(api.friends).items(1):
    print(json.dumps(friend._json, indent=2))

for tweet in tweepy.Cursor(api.user_timeline).items(1):
    print(json.dumps(tweet._json, indent=2))


