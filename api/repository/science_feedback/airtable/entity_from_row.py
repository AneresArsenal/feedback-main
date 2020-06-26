from sqlalchemy_api_handler import humanize
from utils.config import COMMAND_NAME, API_URL, IS_DEVELOPMENT

from models.appearance import Appearance
from models.author_content import AuthorContent
from models.claim import Claim
from models.review import Review
from models.content import Content
from models.medium import Medium
from models.organization import Organization
from models.role import Role, RoleType
from models.user import User
from models.verdict import Verdict
from utils.config import APP_NAME, DEFAULT_USER_PASSWORD, TLD
from utils.random_token import create_random_password


def appearance_from_row(row, unused_index=None):
    reviewed_items = row.get('Item reviewed')
    if not reviewed_items:
        return None

    quoting_content = Content.create_or_modify(
        {'url': row['url'].strip()},
        search_by=['url'])
    medium_science_feedback_ids = row.get('Outlet')
    if medium_science_feedback_ids:
        medium = Medium.query.filter_by(
            scienceFeedbackIdentifier=medium_science_feedback_ids[0]).first()
        quoting_content.mediumId = medium.id

    author_science_feedback_ids = row.get('Authors')
    if author_science_feedback_ids:
        for author_science_feedback_id in author_science_feedback_ids:
            author = User.query.filter_by(
                scienceFeedbackIdentifier=author_science_feedback_id).first()
            author_content = AuthorContent.create_or_modify({
                'authorId': humanize(author.id),
                'contentId': humanize(quoting_content.id)
            }, search_by=['authorId', 'contentId'])
            quoting_content.authorContents = quoting_content.authorContents + [author_content]

    quoted_claim = Claim.query.filter_by(
        scienceFeedbackIdentifier=reviewed_items[0]).first()
    quoted_content = None
    if not quoted_claim:
        quoted_content = Content.query.filter_by(
            scienceFeedbackIdentifier=reviewed_items[0]).first()
    if not quoted_claim and not quoted_content:
        return None

    testifier_science_feedback_ids = row.get('Verified by')
    if not testifier_science_feedback_ids:
        return None
    testifier = User.query.filter_by(
        scienceFeedbackIdentifier=testifier_science_feedback_ids[0]).first()
    if not testifier:
        return None


    if IS_DEVELOPMENT:
        quoting_content.externalThumbUrl = API_URL + '/static/logo.png' if IS_DEVELOPMENT else None
        quoting_content.title = "/".join(quoting_content.url\
                                               .replace('http://', '') \
                                               .replace('https://', '') \
                                               .split('/')[-2:]) \
                                               .replace('-', ' ')

    appearance_dict = {
        'quotedClaim': quoted_claim,
        'quotedContent': quoted_content,
        'quotingContent': quoting_content,
        'scienceFeedbackIdentifier': row['airtableId'],
        'testifier': testifier
    }

    return Appearance.create_or_modify(appearance_dict, search_by='scienceFeedbackIdentifier')


def author_from_row(row, index=None):
    chunks = row['Name'].split(' ')
    first_name = '{}test'.format(COMMAND_NAME).title() if IS_DEVELOPMENT \
                 else chunks[0]
    last_name = 'Author{}'.format(index) if IS_DEVELOPMENT \
                else ' '.join(chunks[1:]).replace('\'', '')
    user_dict = {
        'email': '{}.{}@{}.{}'.format(
            first_name.lower(),
            last_name.lower(),
            APP_NAME,
            TLD),
        'firstName': first_name,
        'lastName': last_name,
        'scienceFeedbackIdentifier': row['airtableId']
    }

    user = User.create_or_modify(user_dict, search_by='email')
    if not user.id:
        user.set_password(DEFAULT_USER_PASSWORD if IS_DEVELOPMENT else create_random_password())

    role = Role.create_or_modify({
        'type': RoleType.AUTHOR,
        'userId': humanize(user.id)
    }, search_by=['type', 'userId'])
    user.role = role

    return user


def claim_from_row(row, unused_index=None):
    text = row.get('Claim checked (or Headline if no main claim)')
    if not text:
        return None

    claim_dict = {
        'scienceFeedbackIdentifier': row['airtableId'],
        'text': text
    }

    return Claim.create_or_modify(claim_dict, search_by='scienceFeedbackIdentifier')


def editor_from_row(row, index=None):
    chunks = row['Name'].split(' ')
    first_name = '{}test'.format(COMMAND_NAME).title() if IS_DEVELOPMENT \
                 else chunks[0]
    last_name = 'Editor{}'.format(index) if IS_DEVELOPMENT \
                else ' '.join(chunks[1:]).replace('\'', '')
    user_dict = {
        'email': '{}.{}@{}.{}'.format(
            first_name.lower(),
            last_name.lower(),
            APP_NAME,
            TLD),
        'firstName': first_name,
        'lastName': last_name,
        'scienceFeedbackIdentifier': row['airtableId']
    }

    user = User.create_or_modify(user_dict, search_by='email')
    if not user.id:
        user.set_password(DEFAULT_USER_PASSWORD if IS_DEVELOPMENT else create_random_password())

    role = Role.create_or_modify({
        'type': RoleType.EDITOR,
        'userId': humanize(user.id)
    }, search_by=['type', 'userId'])
    user.role = role

    return user


def outlet_from_row(row, unused_index=None):
    medium_dict = {
        'name': row['Name'],
        'scienceFeedbackIdentifier': row['airtableId']
    }

    return Medium.create_or_modify(medium_dict, search_by='scienceFeedbackIdentifier')


def review_from_row(row, unused_index=None):
    science_feedback_reviewer_ids = row.get('Review editor(s)')
    if not science_feedback_reviewer_ids:
        return None
    reviewer = User.query.filter_by(
        scienceFeedbackIdentifier=science_feedback_reviewer_ids[0]).first()
    if not reviewer:
        return None

    claim = Claim.query.filter_by(
        scienceFeedbackIdentifier=row['Items reviewed'][0]).first()
    if not claim:
        return None

    review_dict = {
        'claim': claim,
        'scienceFeedbackIdentifier': row['airtableId'],
        'reviewer': reviewer
    }

    return Review.create_or_modify(review_dict, search_by='scienceFeedbackIdentifier')


def reviewer_from_row(row, index=None):
    first_name = '{}test'.format(COMMAND_NAME).title() if IS_DEVELOPMENT \
                 else row['First name']
    last_name = 'Reviewer{}'.format(index) if IS_DEVELOPMENT \
                else row['Last name']
    user_dict = {
        'email': '{}.{}@{}.{}'.format(
            first_name.lower(),
            last_name.lower(),
            APP_NAME,
            TLD) if IS_DEVELOPMENT else row['Email'],
        'firstName': first_name,
        'lastName': last_name,
        'scienceFeedbackIdentifier': row['airtableId']
    }

    user = User.create_or_modify(user_dict, search_by='email')
    if not user.id:
        user.set_password(DEFAULT_USER_PASSWORD if IS_DEVELOPMENT else create_random_password())

    role = Role.create_or_modify({
        'type': RoleType.REVIEWER,
        'userId': humanize(user.id)
    }, search_by=['type', 'userId'])
    user.role = role

    return user


def social_from_row(row, unused_index=None):
    if 'url' not in row:
        return None

    organization_name = row['url'].replace('https://www.', '') \
                                  .split('/')[0] \
                                  .split('.')[0] \
                                  .title()
    organization = Organization.create_or_modify(
        {'name': organization_name},
        search_by='name')

    medium_dict = {
        'name': row['Name'],
        'organization': organization,
        'scienceFeedbackIdentifier': row['airtableId'],
        'url': row['url']
    }

    return Medium.create_or_modify(medium_dict, search_by='scienceFeedbackIdentifier')


def verdict_from_row(row, unused_index=None):
    science_feedback_editor_ids = row.get('Review editor(s)')
    if not science_feedback_editor_ids:
        return None
    editor = User.query.filter_by(scienceFeedbackIdentifier=science_feedback_editor_ids[0]).first()
    if not editor:
        return None

    claim = Claim.query.filter_by(scienceFeedbackIdentifier=row['Items reviewed'][0]).first()
    if not claim:
        return None

    verdict_dict = {
        'claim': claim,
        'editor': editor,
        'scienceFeedbackIdentifier': row['airtableId'],
        'scienceFeedbackUrl': row['Review url'],
        'title': row['Review headline']
    }

    return Verdict.create_or_modify(verdict_dict, search_by='scienceFeedbackIdentifier')
