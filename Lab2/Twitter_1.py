import tweepy
import json
import ConfigParser 
	
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

Config = ConfigParser.ConfigParser()
Config.read("configuration.ini")
print Config.sections()

consumer_key = ConfigSectionMap("TwitterAPI")['consumerkey']
consumer_secret = ConfigSectionMap("TwitterAPI")['consumersecret']
access_token = ConfigSectionMap("TwitterAPI")['accesstoken']
access_secret = ConfigSectionMap("TwitterAPI")['accesstokensecret']

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
  
api = tweepy.API(auth)

user = api.me()
 
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.followers_count))
print('Created: ' + str(user.created_at))
print('Description: ' + str(user.description))


