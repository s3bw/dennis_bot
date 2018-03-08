import os
import logging

import praw


logging.basicConfig(filename='dennis_log', level=logging.INFO)


def auth():
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
    reddit = auth()
    logging.info("Reading Reddit.")

    corpus = []
    subreddits = os.environ.get('REDDIT_SUBREDDITS').split(',')

    for subreddit in subreddits:
        for index, comment in enumerate(reddit.subreddit(subreddit).stream.comments()):
            entry = [subreddit, comment.body]
            corpus.append(entry)

            if index == 99:
                # logging.info("Done {}".format(subreddit))
                break

    corpus = [(
        item[0],
        item[1].encode().decode().strip(),
        len(item[1])
        )
        for item in corpus
    ]

    return corpus

