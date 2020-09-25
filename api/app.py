import os
from flask import Flask

from utils.config import IS_DEVELOPMENT
from utils.setup import setup


FLASK_APP = Flask(__name__, static_url_path='/static')


setup(FLASK_APP,
      with_cors=True,
      with_keywords=True,
      with_login_manager=True,
      with_routes=True)


if __name__ == '__main__':
    FLASK_APP.run(debug=IS_DEVELOPMENT,
                  host='0.0.0.0',
                  port=int(os.environ.get('PORT', 5000)),
                  use_reloader=True)
