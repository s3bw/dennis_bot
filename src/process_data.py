import hashlib
from datetime import datetime


CATEGORY = 'subreddit'
TEXT_FIELD = 'text'
DATA_LENGTH = 'length_text'
ID_FIELD = 'text_id'
ENTRY_DATE = 'entry_date'


REJECT_WORDS = [
    'www',
    'https',
    'reddit',
    'subreddit',
    'OP',
    'r/',
    'I am a bot',
]

def tuple_to_dict(data):
    """ Changes list of tuples to list of dicts

    Example:
        data = [('fake', 'data', 15)]
        return: ['category': 'fake',
                 'text': 'data',
                 'length': 15}]
    Args:
        data list[tuple]: data to be categorized.

    Return:
        list[dict]
    """
    return [{CATEGORY: subreddit,
             TEXT_FIELD: text,
             DATA_LENGTH: length_text}
             for subreddit, text, length_text in data]


def clean_text(row, field):
    """ Remove new line and double space characters.

    Args:
        row dict: containing data to be cleaned.
        field string: containing which data to clean.
    """
    row[field] = row[field].replace('\n', ' ').replace('  ', '')
    if row[field][-1] not in '.?!':
        row[field] =  row[field] + '.'
        
    return row


def valid_row(row):
    if row[DATA_LENGTH] <= 10:
        return False
    for invalid_word in REJECT_WORDS:
        if invalid_word in row[TEXT_FIELD]:
            return False
    return True


def list_dict_items(row):
    """ Create a list of a dict values.

    Example:
        row = [{'A': 'Fake', 'B': 'Data'}]
        return: ['Fake', 'Data']
    """
    return sorted([str(value) for _, value in row.items()])


def hash_row(row):
    row_value = ','.join(list_dict_items(row)).encode('utf-8')
    row[ID_FIELD] = hashlib.sha1(row_value).hexdigest()
    return row


def stamp_time(row):
    row[ENTRY_DATE] = datetime.now()
    return row


def process_new_data(new_data):
    new_data = tuple_to_dict(new_data)
    new_data = [clean_text(row, 'text') for row in new_data]
    new_data = [hash_row(row) for row in new_data if valid_row(row)]
    return [stamp_time(row) for row in new_data]
    
