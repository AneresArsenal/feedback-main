from datetime import datetime
from glob import glob
import json
import os
from sqlalchemy_api_handler import logger

from utils.tmp import TMP_PATH


JOBS_PATH = TMP_PATH / 'jobs'

if not os.path.exists(JOBS_PATH):
    os.makedirs(JOBS_PATH)


def _construct_job_obj(job):
    job_obj = {}
    job_obj['id'] = job.id
    job_obj['name'] = job.name
    job_obj['next_run'] = str(job.next_run_time)
    job_obj['trigger'] = str(job.trigger)
    return job_obj


def get_all_jobs(app):
    async_jobs = app.async_scheduler.get_jobs()
    background_jobs = app.background_scheduler.get_jobs()
    jobs = {'async': [], 'background': [], 'time_recorded': None}

    for job in async_jobs:
        jobs['async'].append(_construct_job_obj(job))
    for job in background_jobs:
        jobs['background'].append(_construct_job_obj(job))
    jobs['time_recorded'] = datetime.now().isoformat()

    return jobs


def remove_oldest_jobs_file(file_limit=5):
    jobs_files = glob(f'{JOBS_PATH}/*.json')
    jobs_files.sort()
    if len(jobs_files) > file_limit:
        os.remove(jobs_files[0])


def write_jobs_to_file(jobs):
    jobs_str = json.dumps(jobs)
    current_time = datetime.now().isoformat()
    job_file = open(f'{JOBS_PATH}/{current_time}.json', 'w')
    job_file.write(jobs_str)
    job_file.close()
