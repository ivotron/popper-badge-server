#!/usr/bin/env python
import os

from flask import Flask, jsonify, request, redirect
from tinydb import TinyDB, Query


app = Flask(__name__)


@app.route('/<org>/<repo>', methods=['GET', 'POST'])
def index(org, repo):
    """Handles root url route of the server.

    Supported methods:
        GET: Redirects to badge svg image url from https://shields.io
        POST: Records the entry for org/repo in the database
    """
    if request.method == 'GET':

        db = TinyDB(app.config.get('DB_NAME', 'db.json'))
        Record = Query()
        records = sorted(
            db.search(Record.name == '{}/{}'.format(org, repo)),
            key=lambda x: x['timestamp']
        )
        color_codes = {
            'OK': 'green',
            'GOLD': 'yellow',
            'FAIL': 'red'
        }
        if len(records) > 0:
            status = records[-1]['status']
            return redirect(
                'https://img.shields.io/badge/Popper-{}-{}.svg'
                .format(status, color_codes[status])
            )
        else:
            return redirect(
                'https://img.shields.io/badge/Popper-undefined-lightgrey.svg'
            )

    elif request.method == 'POST':

        commit_id = request.form.get('commit_id', None)
        timestamp = request.form.get('timestamp', None)
        status = request.form.get('status', None)

        if not commit_id or not timestamp or not status:
            return jsonify({
                'message': "Please provide commit id, timestamp and status."
            }), 400
        else:
            db = TinyDB(app.config.get('DB_NAME', 'db.json'))
            db.insert({
                'name': '{}/{}'.format(org, repo),
                'commit_id': commit_id,
                'timestamp': timestamp,
                'status': status
            })
            return jsonify({
                'message': "Record successfully created."
            }), 201


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
        del record['timestamp']
        del record['name']

    return jsonify(records)


if __name__ == '__main__':
    app.run(debug=True)
