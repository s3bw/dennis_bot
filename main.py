import sys
import time

from time import strftime
from datetime import (
    date,
    datetime,
    timedelta,
)

import tweepy
import configparser

config = configparser.ConfigParser()
config.read('config.cfg')

CONSUMER_KEY = config.get('CONSUMER', 'KEY')
CONSUMER_SECRET = config.get('CONSUMER', 'SECRET')

ACCESS_KEY = config.get('ACCESS', 'KEY')
ACCESS_SECRET = config.get('ACCESS', 'SECRET')

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

api.update_status('200')

