from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sqlalchemy import and_, func, Index, TEXT
from sqlalchemy.sql.expression import cast, or_
from sqlalchemy.sql.functions import coalesce


LANGUAGE = 'english'
STOP_WORDS = set(stopwords.words(LANGUAGE))


def create_fts_index(name, ts_vector):
    return Index(name,
                 ts_vector,
                 postgresql_using='gin')


def create_tsvector(*args):
    exp = args[0]
    for e in args[1:]:
        exp += ' ' + e
    return func.to_tsvector(LANGUAGE + '_unaccent', exp)


def create_ts_vector_and_table_args(ts_indexes):
    ts_vectors = []
    table_args = []

    for ts_index in ts_indexes:
        ts_vector = create_tsvector(ts_index[1])
        ts_vectors.append(ts_vector)
        table_args.append(create_fts_index(ts_index[0], ts_vector))

    return ts_vectors, tuple(table_args)



def ts_queries_from_keywords_string(keywords_string):

    keywords = word_tokenize(keywords_string)
    keywords_without_stop_words = [
        keyword
        for keyword in keywords
        if keyword.lower() not in STOP_WORDS
    ]

    ts_queries = ['{}:*'.format(keyword) for keyword in keywords_without_stop_words]

    return ts_queries
