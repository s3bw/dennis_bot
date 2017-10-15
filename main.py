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


def validate_tweet(tweet):
    reject_words = [
       'subreddit',
       'OP',
    ]

    for word in reject_words:
        if word in tweet:
            return False

        if word.capitalize() in tweet:
            return False
    return True


def construct_tweet():
    time1 = time.time()
    api = auth_twitter()
    corpus = research_corpus()
    text_model = markovify.Text(corpus)

    isValid = False
    while isValid == False:
        status_tweet = text_model.make_short_sentence(120, tries=25)
        isValid = validate_tweet(status_tweet)
        print('Tweet: {}'.format(isValid))
        if isValid == False:
            print(status_tweet)

    time2 = time.time()
    print('{} {:.2f}'.format(status_tweet, time2-time1))
    # api.update_status(status_tweet)


if __name__ == '__main__':

    schedule.every().day.at("18:30").do(construct_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)
