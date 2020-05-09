from sqlalchemy import BigInteger,\
                       Column,\
                       ForeignKey,\
                       Text
from sqlalchemy.orm import relationship
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy_api_handler import ApiHandler
from sqlalchemy_api_handler.mixins.soft_deletable_mixin import SoftDeletableMixin
from sqlalchemy.orm.collections import InstrumentedList
from models.utils.db import get_model_with_table_name, Model
from models.mixins import HasRatingMixin


class Verdict(ApiHandler,
              Model,
              HasRatingMixin,
              SoftDeletableMixin):

    articleId = Column(BigInteger(),
                       ForeignKey('article.id'),
                       nullable=False,
                       index=True)

    article = relationship('Article',
                           foreign_keys=[articleId],
                           backref='verdicts')

    comment = Column(Text(), nullable=True)

    editorId = Column(BigInteger(),
                      ForeignKey('user.id'),
                      nullable=False,
                      index=True)

    editor = relationship('User',
                          foreign_keys=[editorId],
                          backref='verdics')

    @property
    def reviews(self):
        Review = get_model_with_table_name('review')
        verdict_reviewer_ids = [
            verdictReviewer.reviewer.id
            for verdictReviewer in self.verdictReviewers
        ]
        reviews = Review.query.filter(
            (Review.articleId == self.articleId) &\
            (Review.reviewerId.in_(verdict_reviewer_ids))
        ).all()

        return InstrumentedList(reviews)
