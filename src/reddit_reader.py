import configparser

import praw

config = configparser.ConfigParser()
config.read('reddit_config.cfg')

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

print('Reading Reddit:')

CORPUS = []

subreddits = config.get('REDDIT', 'SUBREDDITS').split(',')

for subreddit in subreddits:
    for index, comment in enumerate(reddit.subreddit(subreddit).stream.comments()):
        CORPUS.append(comment.body)
        if index == 99:
            print('Done {}'.format(subreddit))
            break

CORPUS = [item.encode().decode() for item in CORPUS]

with open('corpus_data.txt', 'w', encoding='utf-8') as output_data:
    for item in CORPUS:
        output_data.write(item)

