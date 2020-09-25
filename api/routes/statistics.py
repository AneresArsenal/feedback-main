from flask import current_app as app, jsonify

from repository.statistics import get_global_statistics


@app.route('/statistics', methods=['GET'])
def get_statistics():
    return jsonify(get_global_statistics)
