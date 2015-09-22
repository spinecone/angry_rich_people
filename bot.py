from angry_sentence import formatted_angry_review
import tweepy
from secrets import *

def find_review():
  return formatted_angry_review()

def tweet(message):
  auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  auth.set_access_token(access_key, access_secret)
  api = tweepy.API(auth)
  auth.secure = True
  print("Posting message {}".format(message))
  api.update_status(status=message)

tweet(find_review())