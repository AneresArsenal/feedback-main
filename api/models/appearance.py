import enum
from sqlalchemy import BigInteger, \
                       Column, \
                       Enum, \
                       ForeignKey
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship
from sqlalchemy_api_handler import ApiHandler

from models.mixins import HasScienceFeedbackMixin
from utils.db import Model


class StanceType(enum.Enum):
    ENDORSEMENT = {
        'label': 'endorsement',
        'value': 1
    }
    NEUTRAL = {
        'label': 'neutral',
        'value': 0
    }
    REFUSAL = {
        'label': 'refusal',
        'value': -1
    }


class Appearance(ApiHandler,
                 Model,
                 HasScienceFeedbackMixin):

    contentId = Column(BigInteger(),
                     ForeignKey('content.id'),
                     nullable=False,
                     index=True)

    content = relationship('Content',
                         foreign_keys=[contentId],
                         backref='appearances')


    claimId = Column(BigInteger(),
                     ForeignKey('claim.id'),
                     nullable=False,
                     index=True)

    claim = relationship('Claim',
                         foreign_keys=[claimId],
                         backref='appearances')

    stance = Column(Enum(StanceType))


    testifierId = Column(BigInteger(),
                         ForeignKey('user.id'),
                         nullable=False,
                         index=True)

    testifier = relationship('User',
                             foreign_keys=[testifierId],
                             backref='appearances')
