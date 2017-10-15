import time
import configparser

import tweepy
import schedule
import markovify

from src.reddit_reader import research_corpus


def auth_twitter():
    config = configparser.ConfigParser()
    config.read('config.cfg')

    CONSUMER_KEY = config.get('CONSUMER', 'KEY')
    CONSUMER_SECRET = config.get('CONSUMER', 'SECRET')

    ACCESS_KEY = config.get('ACCESS', 'KEY')
    ACCESS_SECRET = config.get('ACCESS', 'SECRET')

    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    return tweepy.API(auth)


def construct_tweet():
    api = auth_twitter()
    corpus = research_corpus()
    text_model = markovify.Text(corpus)

    status_tweet = text_model.make_short_sentence(120, tries=25)
    
    print(status_tweet)
    # api.update_status(status_tweet)


if __name__ == '__main__':

    schedule.every().day.at("23:59").do(construct_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)
