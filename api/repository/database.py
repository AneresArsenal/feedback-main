from sqlalchemy_api_handler import logger

from repository import import_keywords
from utils.activity import import_activity
from utils.db import db


def clean():
    logger.info('clean all the database...')
    for table in reversed(db.metadata.sorted_tables):
        print("Clearing table {table_name}...".format(table_name=table))
        db.session.execute(table.delete())

    db.session.commit()
    logger.info('clean all the database...Done.')


def create():
    logger.info('create all the database...')
    import_activity()
    import_keywords()
    db.create_all()
    db.session.commit()
    logger.info('create all the database...Done.')
