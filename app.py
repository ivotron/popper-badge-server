#!/usr/bin/env python
import time

from flask import Flask, jsonify, request, render_template, make_response
from tinydb import TinyDB, Query
from wsgiref.handlers import format_date_time


app = Flask(__name__)


BADGE_NAMES = {
    'SUCCESS': 'popper-SUCCESS-green',
    'GOLD': 'popper-GOLD-yellow',
    'FAIL': 'popper-FAIL-red'
}


@app.route('/<org>/<repo>', methods=['GET', 'POST'])
def index(org, repo):
    """Handles root url route of the server.

    Supported methods:
        GET: Serve the badge svg image
        POST: Records the entry for org/repo in the database
    """
    if request.method == 'GET':

        db = TinyDB(app.config.get('DB_NAME', 'db.json'))
        Record = Query()
        records = sorted(
            db.search(Record.name == '{}/{}'.format(org, repo)),
            key=lambda x: x['timestamp']
        )

        if len(records) > 0:
            status = records[-1]['status']
            timestamp = time.gmtime(int(records[-1]['timestamp']))
            svg = render_template(
                BADGE_NAMES.get(status, 'popper-undefined-lightgrey') + '.svg'
            )
        else:

            svg = render_template('popper-undefined-lightgrey.svg')
            timestamp = time.gmtime(0)

        response = make_response(svg)
        response.content_type = 'image/svg+xml'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Last-Modified'] = format_date_time(
            time.mktime(timestamp)
        )
        return response

    elif request.method == 'POST':

        commit_id = request.form.get('commit_id', None)
        timestamp = request.form.get('timestamp', None)
        status = request.form.get('status', None)
        branch = request.form.get('branch', None)

        if not commit_id or not timestamp or not status or not branch:

            return jsonify({
                'message': "Please provide commit id,"
                " timestamp, branch and status."
            }), 400

        else:

            db = TinyDB(app.config.get('DB_NAME', 'db.json'))

            if branch == 'master':

                # Check if the commit id already exists, update if present
                Record = Query()
                records = db.search(Record.name == '{}/{}'.format(org, repo))
                record_exists = False
                for record in records:
                    if record['commit_id'] == commit_id:
                        record_exists = True
                        record['status'] = status
                        record['timestamp'] = timestamp
                        db.update(
                            record, (Record.name == '{}/{}'.format(org, repo))
                            & (Record.commit_id == commit_id)
                        )
                        break

                # If record doesn't exist with same commit id, create a new one
                if not record_exists:
                    db.insert({
                        'name': '{}/{}'.format(org, repo),
                        'commit_id': commit_id,
                        'timestamp': timestamp,
                        'status': status
                    })

                return jsonify({
                    'message': "Record successfully created."
                }), 201

            else:

                return jsonify({
                    'message': "Record received but not saved."
                }), 200


@app.route('/<org>/<repo>/list', methods=['GET'])
def list_records(org, repo):
    """List the records for a particular org/repo.
    Only the commit_id and status is returned.

    Returns:
        List of records in the form of JSON data
    """
    db = TinyDB(app.config.get('DB_NAME', 'db.json'))
    Record = Query()
    records = sorted(
        db.search(Record.name == '{}/{}'.format(org, repo)),
        key=lambda x: x['timestamp']
    )
    for record in records:
        record['timestamp'] = time.strftime(
            '%Y-%m-%d %H:%M:%S', time.localtime(int(record['timestamp']))
        )
        del record['name']

    return jsonify(records)


if __name__ == '__main__':
    app.run(debug=True)
