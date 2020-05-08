import pytest
from sqlalchemy_api_handler import ApiHandler

from models.appearance import Appearance
from models.article import Article
from models.claim import Claim
from models.review import Review
from models.user import User
from repository.science_feedback import sync
from tests.utils.clean import with_clean_all_database


@pytest.mark.standalone
@with_clean_all_database
def when_sync_all_is_a_success(app):
    # when
    sync()

    # then
    for model in [Claim, User]:
        print(model, len(model.query.all()))
        assert len(model.query.all()) > 0
