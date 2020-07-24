from models.tag import Tag
from models.user import User
from models.verdict import Verdict
from models.verdict_tag import VerdictTag

from domain.keywords import create_filter_matching_all_keywords_in_any_model, \
                            create_get_filter_matching_ts_query_in_any_model


VERDICT_TS_FILTER = create_get_filter_matching_ts_query_in_any_model(
    Verdict,
    Tag,
    User
)


def get_verdicts_join_query(query):
    query = query.outerjoin(VerdictTag) \
                 .outerjoin(Tag) \
                 .join(User)
    return query


def keep_verdict_with_keywords(query, keywords):
    keywords_filter = create_filter_matching_all_keywords_in_any_model(
        VERDICT_TS_FILTER,
        keywords
    )

    query = query.filter(keywords_filter)
    return query
