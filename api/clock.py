import asyncio
import atexit
import time
from flask import Flask

from sqlalchemy_api_handler import logger
from utils.jobs import get_all_jobs, write_jobs_to_file, remove_oldest_jobs_file
from utils.setup import setup


CLOCK_APP = Flask(__name__)

setup(CLOCK_APP, with_jobs=True)

if __name__ == '__main__':
    CLOCK_APP.async_scheduler.start()
    CLOCK_APP.background_scheduler.start()
    atexit.register(lambda: CLOCK_APP.async_scheduler.shutdown())
    atexit.register(lambda: CLOCK_APP.background_scheduler.shutdown())

    try:
        asyncio.get_event_loop().run_forever()
        while True:
            jobs = get_all_jobs(CLOCK_APP)
            write_jobs_to_file(jobs)
            remove_oldest_jobs_file()
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Scheduler interupted')
