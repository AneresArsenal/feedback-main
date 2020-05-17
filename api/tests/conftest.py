import pytest
from flask import Flask
from flask_login import LoginManager
from sqlalchemy_api_handler import ApiHandler

from utils.setup import setup


items_by_category = {'first': [], 'last': []}

def _sort_alphabetically(category):
    return sorted(items_by_category[category], key=lambda item: item.location)


def pytest_collection_modifyitems(config, items):
    """
    This function can be deleted once the tests are truly order-independent.
    :param items: Test items parsed by pytest, available for sorting
    """
    for item in items:
        if 'standalone' in item.keywords:
            items_by_category['last'].append(item)
        else:
            items_by_category['first'].append(item)

    print('\n************************************************************')
    print('*                                                          *')
    print('*  %s tests are still depending on the execution order     *' % len(items_by_category['first']))
    print('*                                                          *')
    print('************************************************************')
    items[:] = _sort_alphabetically('first') + _sort_alphabetically('last')


@pytest.fixture(scope='session')
def app():
    flask_app = Flask(__name__)
    flask_app.config['TESTING'] = True

    setup(flask_app,
          with_login_manager=True,
          with_routes=True)

    return flask_app
