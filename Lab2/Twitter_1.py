import tweepy
from tweepy import OAuthHandler
 
consumer_key = '9bzcmNQRJD7XJ2GGJLff0lQPn'
consumer_secret = '0fnkzhgTIKO9J8Rv1ACh0xlfzexiWwAtJkZuqi63Bps8HpcUdc'
access_token = '238985389-gmnDbJER33buDhPq6cMmOlSbU5kCLnQUO4FkWUBO'
access_secret = 'EDGAt0k3WrxqG9dfLKTAlqRmAZtxK95OEPn3Ud2zSr7oQ'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
  
api = tweepy.API(auth)

user = api.me()
 
print('Name: ' + user.name)
print('Location: ' + user.location)
print('Friends: ' + str(user.followers_count))
print('Created: ' + str(user.created_at))
print('Description: ' + str(user.description))
