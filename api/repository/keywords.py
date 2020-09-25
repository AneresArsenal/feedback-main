from flask_sqlalchemy import BaseQuery
from sqlalchemy import func
from sqlalchemy.sql.expression import cast, and_, or_
from sqlalchemy.sql.functions import coalesce

from domain.keywords import ts_queries_from_keywords_string, \
                            LANGUAGE

"""
def get_first_matching_any_ts_queries_at_column(query, ts_queries, column):
    ts_vector = func.to_tsvector(cast(coalesce(column, ''), TEXT))
    ts_queries_filter = or_(
        *[
            ts_vector.match(ts_query, postgresql_regconfig=LANGUAGE)
            for ts_query in ts_queries
        ]
    )
    return query.filter(ts_queries_filter).first()


def get_first_matching_keywords_string_at_column(query, keywords_string, column):
    ts_queries = ts_queries_from_keywords_string(keywords_string)
    return get_first_matching_any_ts_queries_at_column(query, ts_queries, column)
"""

def create_get_filter_matching_ts_query_in_any_model(*models):
    def get_filter_matching_ts_query_in_any_model(ts_query):
        return or_(
            *[
                model.__ts_vector__.match(
                    ts_query,
                    postgresql_regconfig=LANGUAGE
                )
                for model in models
            ]
        )
    return get_filter_matching_ts_query_in_any_model


def create_filter_matching_all_keywords_in_any_model(get_filter_matching_ts_query_in_any_model,
                                                     keywords_string):
    ts_queries = ts_queries_from_keywords_string(keywords_string)
    ts_filters = [
        get_filter_matching_ts_query_in_any_model(ts_query)
        for ts_query in ts_queries
    ]
    return and_(*ts_filters)
