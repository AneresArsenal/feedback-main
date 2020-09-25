from datetime import datetime, timedelta
from sqlalchemy_api_handler import ApiHandler, logger

from models.content import Content
from models.content_tag import ContentTag
from models.tag import Tag

from domain.content import newspaper_from_url
from domain.trendings.buzzsumo import buzzsumo_trending_from_url
from repository.activities import filter_by_activity_date_and_verb
from repository.crowdtangle import attach_crowdtangle_entities_from_content
from repository.keywords import create_filter_matching_all_keywords_in_any_model, \
                                create_get_filter_matching_ts_query_in_any_model
from utils.screenshotmachine import capture
from utils.wayback_machine import url_from_archive_services
from storage.thumb import save_thumb


CONTENT_TS_FILTER = create_get_filter_matching_ts_query_in_any_model(Content,
                                                                     Tag)


def content_from_url(url,
                     sync_crowdtangle=False,
                     **kwargs):
    content = Content.create_or_modify({
        '__SEARCH_BY__': 'url',
        'url': url
    })

    if sync_crowdtangle:
        attach_crowdtangle_entities_from_content(content,
                                                 request_start_date='2019-09-01')

    trending = buzzsumo_trending_from_url(url, **kwargs)
    if trending:
        return content.modify(trending)

    if url:
        newspaper = newspaper_from_url(url, **kwargs)
        if newspaper:
            return content.modify(newspaper)

    content.urlNotFound = True
    return content


def get_contents_keywords_join_query(query):
    query = query.outerjoin(ContentTag)\
                 .outerjoin(Tag)
    return query


def keep_contents_with_keywords(query, keywords):
    keywords_filter = create_filter_matching_all_keywords_in_any_model(CONTENT_TS_FILTER,
                                                                       keywords)
    query = query.filter(keywords_filter)
    return query


def keep_contents_with_minimal_datum(query):
    return query.filter((Content.title is not None) & \
                        ((Content.externalThumbUrl is not None) | (Content.thumbCount > 0)))


def filter_contents_by_is_reviewable(query, is_reviewable):
    query = query.filter_by(isReviewable=is_reviewable)
    return query


def sync_content(content,
                 sync_archive_url=False,
                 sync_crowdtangle=False,
                 sync_thumbs=False,
                 session=None):
    content = content_from_url(content.url, sync_crowdtangle=sync_crowdtangle)
    if content.url:
        if not content.externalThumbUrl and content.thumbCount == 0 and sync_thumbs:
            thumb = capture(content.url)
            save_thumb(content, thumb, 0, convert=False)
        if not content.archiveUrl and sync_archive_url:
            content.archiveUrl = url_from_archive_services(content.url)
    ApiHandler.save(content)
    return content


def sync(from_date=None,
         to_date=None,
         sync_archive_url=False,
         sync_crowdtangle=False,
         sync_thumbs=False,
         contents_max=None):
    now_date = datetime.utcnow()
    if from_date is None:
        from_date = now_date - timedelta(hours=12)
    if to_date is None:
        to_date = now_date - timedelta(minutes=0)

    query = Content.query.filter(Content.type==None).order_by(Content.id.desc())

    if from_date or to_date:
        query = filter_by_activity_date_and_verb(query,
                                                 from_date=from_date,
                                                 to_date=to_date,
                                                 verb='insert')

    contents = query.all()

    if contents_max is None:
        contents_max = len(contents)

    logger.info(f'Sync contents from {from_date} to {to_date}...')
    for content in contents[:contents_max]:
        sync_content(
            content,
            sync_archive_url=sync_archive_url,
            sync_crowdtangle=sync_crowdtangle,
            sync_thumbs=sync_thumbs
        )
        logger.info(f'Synced content: {content.id}')

    logger.info(f'Sync contents from {from_date} to {to_date}...Done')
