from sqlalchemy import BigInteger, Column, ForeignKey
from sqlalchemy.orm import backref, relationship
from sqlalchemy_api_handler import ApiHandler

from utils.db import db


class UserTag(ApiHandler,
              db.Model):

    userId = Column(BigInteger(),
                    ForeignKey('user.id'),
                    primary_key=True)

    user = relationship('User',
                        foreign_keys=[userId],
                        backref=backref("userTags"))

    tagId = Column(BigInteger(),
                   ForeignKey('tag.id'),
                   primary_key=True)

    tag = relationship('Tag',
                       foreign_keys=[tagId],
                       backref=backref("userTags"))
