import atexit
import time

from flask import Flask

from sqlalchemy_api_handler import logger
from utils.jobs import get_all_jobs, \
                       remove_oldest_jobs_file, \
                       write_jobs_to_file

from utils.setup import setup


CLOCK_APP = Flask(__name__)

setup(CLOCK_APP, with_jobs=True)

if __name__ == '__main__':
    # CLOCK_APP.async_scheduler.start()
    CLOCK_APP.background_scheduler.start()
    # atexit.register(lambda: CLOCK_APP.async_scheduler.shutdown())
    atexit.register(CLOCK_APP.background_scheduler.shutdown)
    print_jobs = True

    try:
        while True:
            if print_jobs:
                jobs = get_all_jobs(CLOCK_APP)
                write_jobs_to_file(jobs)
                remove_oldest_jobs_file()
            time.sleep(60)
    except (KeyboardInterrupt, SystemExit):
        logger.warning('Scheduler interupted')
        print_jobs = False
        # CLOCK_APP.async_scheduler.shutdown()
        CLOCK_APP.background_scheduler.shutdown()
