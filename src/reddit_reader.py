import configparser

import praw


def auth_reddit():
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

def research_corpus():
    reddit, config = auth_reddit()

    print('Reading Reddit:')

    corpus = []
    subreddits = config.get('REDDIT', 'SUBREDDITS').split(',')

    for subreddit in subreddits:
        for index, comment in enumerate(reddit.subreddit(subreddit).stream.comments()):
            corpus.append(comment.body)
            if index == 99:
                print('Done {}'.format(subreddit))
                break

    corpus = [item.encode().decode() for item in corpus]
    return '\n'.join(corpus)

