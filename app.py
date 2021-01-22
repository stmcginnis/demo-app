#
# SPDX-License-Identifier: Apache-2.0
#

import json
import os

from flask import Flask, request, jsonify
import pymysql

app = Flask(__name__)


def get_db_connection():
    host = os.environ.get('DB_SERVER', 'db-server')
    db = os.environ.get('MYSQL_DATABASE')
    user = os.environ.get('MYSQL_USER')
    passwd = os.environ.get('MYSQL_PASSWORD')

    con = pymysql.connect(
        host=host,
        db=db,
        user=user,
        password=passwd,
    )
    return con


@app.route('/', methods=['GET'])
def query_records():
    # Get all records from the database
    results = []
    db = get_db_connection()

    try:
        with db.cursor() as cur:
            cur.execute('SELECT * FROM items')
            rows = cur.fetchall()

            for row in rows:
                results.append({
                    'id': row[0],
                    'name': row[1],
                    'descript': row[2],
                })
    except Exception as e:
        print('Error getting records: %s' % e)
    finally:
        db.close

    return jsonify(results)


@app.route('/', methods=['POST'])
def update_record():
    record = json.loads(request.data)
    db = get_db_connection()

    try:
        with db.cursor() as cur:
            cur.execute('INSERT INTO items(name, descript) VALUES(%s, %s)',
                (record['name'], record['description']))
            db.commit()
    except Exception as e:
        print('Error inserting item: %s' % e)
        return jsonify({'result': 'Error: %s' % e})
    finally:
        db.close()
    return jsonify({'result': 'added'})


# @app.route('/', methods=['DELETE'])
# def delte_record():
#     record = json.loads(request.data)
# Find ID in db and delete


app.run(host='0.0.0.0', port=8080, debug=True)
