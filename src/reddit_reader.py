import os
import configparser

import praw


def auth_reddit_locally():
    config = configparser.ConfigParser()
    config.read('config.cfg')

    CLIENT_ID = config.get('REDDIT', 'ID')
    CLIENT_SECRET = config.get('REDDIT', 'SECRET')
    PASSWORD = config.get('REDDIT', 'PASSWORD')
    USERNAME = config.get('REDDIT', 'USER_NAME')

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent='make database with comments.',
        password=PASSWORD,
        username=USERNAME,
    )
    return reddit, config


def auth_reddit_remotely():
    CLIENT_ID = os.environ.get('REDDIT_ID')
    CLIENT_SECRET = os.environ.get('REDDIT_SECRET')
    PASSWORD = os.environ.get('REDDIT_PASSWORD')
    USERNAME = os.environ.get('REDDIT_USER_NAME')

    reddit = praw.Reddit(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        user_agent='make database with comments.',
        password=PASSWORD,
        username=USERNAME,
    )
    return reddit


def research_corpus():
    try:
        reddit, config = auth_reddit_locally()
    except:
        reddit = auth_reddit_remotely()

    print('Reading Reddit:')

    corpus = []
    try:
        subreddits = config.get('REDDIT', 'SUBREDDITS').split(',')
    except:
        subreddits = os.environ.get('REDDIT_SUBREDDITS').split(',')

    for subreddit in subreddits:
        for index, comment in enumerate(reddit.subreddit(subreddit).stream.comments()):
            corpus.append(comment.body)
            if index == 99:
                print('Done {}'.format(subreddit))
                break

    corpus = [item.encode().decode() for item in corpus]
    return '\n'.join(corpus)

