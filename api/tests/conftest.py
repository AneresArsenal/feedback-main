import pytest
from flask import Flask
from flask_login import LoginManager
from sqlalchemy_api_handler import ApiHandler

import sys
print(dir(sys), sys.path)

from domain.content import newspaper_from_url
from utils.setup import setup


ITEMS_BY_CATEGORY = {'first': [], 'last': []}


def _sort_alphabetically(category):
    return sorted(ITEMS_BY_CATEGORY[category], key=lambda item: item.location)


def pytest_collection_modifyitems(config, items):
    """
    This function can be deleted once the tests are truly order-independent.
    :param items: Test items parsed by pytest, available for sorting
    """
    for item in items:
        if 'standalone' in item.keywords:
            ITEMS_BY_CATEGORY['last'].append(item)
        else:
            ITEMS_BY_CATEGORY['first'].append(item)

    print('\n************************************************************')
    print('*                                                          *')
    print('*  %s tests are still depending on the execution order     *' % len(ITEMS_BY_CATEGORY['first']))
    print('*                                                          *')
    print('************************************************************')
    items[:] = _sort_alphabetically('first') + _sort_alphabetically('last')


@pytest.fixture(scope='session')
def app():
    flask_app = Flask(__name__)
    flask_app.config['TESTING'] = True

    setup(flask_app,
          with_keywords=True,
          with_login_manager=True,
          with_routes=True)

    return flask_app
