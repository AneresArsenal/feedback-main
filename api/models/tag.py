import enum
from sqlalchemy import Column, \
                       Enum, \
                       Integer, \
                       String, \
                       Text
from sqlalchemy_api_handler import ApiHandler
from sqlalchemy_api_handler.mixins.soft_deletable_mixin import \
    SoftDeletableMixin

from utils.db import Model


class SourceName(enum.Enum):
    CLAIM = 'claim'
    CONTENT = 'content'


class TagType(enum.Enum):
    CONCLUSION = 'conclusion'
    DETAIL = 'detail'
    EVALUATION = 'evaluation'
    ISSUE = 'issue'
    QUALIFICATION = 'qualification'


class Tag(ApiHandler,
          Model,
          SoftDeletableMixin):

    info = Column(Text(), nullable=True)

    label = Column(String(128))

    positivity = Column(Integer(), nullable=True)

    source = Column(Enum(SourceName))

    type = Column(Enum(TagType))

    value = Column(Integer())
