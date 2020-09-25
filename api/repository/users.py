from sqlalchemy import and_
from sqlalchemy_api_handler import ApiErrors, ApiHandler, logger

from domain.user import store_user_thumb_from_sandbox
from models.role import Role
from models.tag import Tag
from models.user import User
from models.user_tag import UserTag
from repository.keywords import create_filter_matching_all_keywords_in_any_model, \
                                create_get_filter_matching_ts_query_in_any_model
from utils.config import DEFAULT_USER_PASSWORD, IS_DEVELOPMENT
from utils.db import db


user_ts_filter = create_get_filter_matching_ts_query_in_any_model(User,
                                                                  Tag)


def create_default_user():
    default_user = User()
    default_user.set_password(DEFAULT_USER_PASSWORD)
    return default_user


def get_user_with_credentials(identifier, password):
    errors = ApiErrors()
    errors.status_code = 401

    if identifier is None:
        errors.add_error('identifier', 'Identifier is missing.')
    if password is None:
        errors.add_error('password', 'Password is missing.')
    errors.maybe_raise()

    user = User.query.filter_by(email=identifier).first()

    if not user:
        errors.add_error('identifier', 'Wrong identifier')
        raise errors
    if not user.check_password(password):
        errors.add_error('password', 'Wrong password')
        raise errors

    return user


def change_password(user, password):
    if type(user) != User:
        user = User.query.filter_by(email=user).one()
    user.set_password(password)
    user = db.session.merge(user)
    ApiHandler.save(user)


def find_user_by_email(email):
    return User.query.filter_by(email=email).first()


def find_user_by_reset_password_token(token):
    return User.query.filter_by(reset_passwordToken=token).first()


def get_users_join_query(query):
    query = query.outerjoin(UserTag)\
                 .outerjoin(Tag)
    return query


def get_users_query_with_keywords(query, keywords):
    keywords_filter = create_filter_matching_all_keywords_in_any_model(
        user_ts_filter,
        keywords
    )
    query = query.outerjoin(UserTag)\
                 .outerjoin(Tag)\
                 .filter(keywords_filter)
    return query


def keep_users_with_roles(query, roles):
    roles_filter = and_(*[User.roles.any(Role.type == role) for role in roles])
    query = query.filter(roles_filter)
    return query


def keep_users_with_no_role(query):
    query = query.filter(~User.roles.any())
    return query


def sync_user(user):
    if IS_DEVELOPMENT:
        store_user_thumb_from_sandbox(user)


def sync():
    logger.info('sync users data...')
    for user in User.query.all():
        sync_user(user)
    logger.info('sync users data...Done.')
