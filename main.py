import time
import logging

import schedule

import src.postgresql_db as psql
from src import twitter
from src import reddit
from src.process_data import process_new_data
from src import nlp_modelling


logging.basicConfig(filename='dennis_log', level=logging.INFO)


def construct_tweet():
    time1 = time.time()

    corpus = reddit.research_corpus()
    process_corpus = process_new_data(corpus)

    logging.info("length,{}".format(len(process_corpus)))
    connection = psql.auth()
    psql.insert_many(connection, process_corpus)
    
    training_corpus = psql.extract_data(connection)

    tweet_model = nlp_modelling.train(training_corpus)
    status_tweet = nlp_modelling.create_tweet(tweet_model)
    # status_tweet = nlp_modelling.create_response(tweet_model)

    # status_tweet = text_model.make_short_sentence(120, tries=25)
    logging.info("tweet,{}".format(status_tweet))

    time2 = time.time()
    print('{} {:.2f}'.format(status_tweet, time2-time1))

    tweet = twitter.auth()
    tweet.update_status(status_tweet)


if __name__ == '__main__':

    # construct_tweet()
    schedule.every().day.at("17:30").do(construct_tweet)
    schedule.every().hour.do(construct_tweet)
    while True:
        schedule.run_pending()
        time.sleep(1)
