import json
from glob import glob
from flask import current_app as app, jsonify

from utils.jobs import JOBS_PATH


@app.route('/jobs', methods=['GET'])
def get_all_jobs():
    jobs_files = glob(f'{JOBS_PATH}/*.json')
    if not jobs_files:
        return jsonify({'jobs': 'no jobs active'}), 404

    jobs_files.sort()
    jobs = open(jobs_files[-1], 'r')
    jobs_str = jobs.read()
    jobs.close()
    if not jobs_str:
        return jsonify({'jobs': 'jobs content is empty'})

    latest = json.loads(jobs_str)
    return jsonify(latest)
