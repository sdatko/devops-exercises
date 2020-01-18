#!/usr/bin/env python3
# coding=utf-8

from flask import abort
from flask import Flask
from flask import make_response

import json

app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return pretty_json({
        "resources": {
            "matrix": "/matrix/<matrix>",
            "column": "/columns/<matrix>/<column_number>",
            "row": "/rows/<matrix>/<row_number>",
        },
        "current_uri": "/",
        "example": "/matrix/123n456n789",
    })


@app.route("/matrix/<matrix>", methods=['GET'])
def matrix(matrix):
    if not verify_characters(matrix):
        return abort(400, 'Invalid characters in matrix.')
    if not verify_dimensions(matrix):
        return abort(400, 'Invalid matrix dimensions.')

    return matrix.replace('', ' ').replace(' n ', '\n').strip()


@app.route("/columns/<matrix>/<column_number>", methods=['GET'])
def column(matrix, column_number):
    if not verify_characters(matrix):
        return abort(400, 'Invalid characters in matrix.')
    if not verify_dimensions(matrix):
        return abort(400, 'Invalid matrix dimensions.')

    rows, columns = get_dimensions(matrix)
    try:
        column = int(column_number)
    except ValueError:
        return abort(400, 'Incorrect value given as column number.')
    if column < 1 or column > columns:
        return abort(400, 'Wrong column number requested.')

    column_index = column - 1
    return '\n'.join([row[column_index] for row in matrix.split('n')])


@app.route("/rows/<matrix>/<row_number>", methods=['GET'])
def row(matrix, row_number):
    if not verify_characters(matrix):
        return abort(400, 'Invalid characters in matrix.')
    if not verify_dimensions(matrix):
        return abort(400, 'Invalid matrix dimensions.')

    rows, columns = get_dimensions(matrix)
    try:
        row = int(row_number)
    except ValueError:
        return abort(400, 'Incorrect value given as row number.')
    if row < 1 or row > rows:
        return abort(400, 'Wrong row number requested.')

    row_index = row - 1
    return matrix.split('n')[row_index].replace('', ' ').strip()


def pretty_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


def verify_characters(string):
    characters = set(string)
    accepted_characters = set('1234567890n')

    invalid_characters = characters - accepted_characters

    if len(invalid_characters) > 0:
        return False
    else:
        return True


def verify_dimensions(matrix):
    rows = matrix.split('n')
    columns = set()

    for row in rows:
        columns.add(len(row))

    if len(columns) != 1:
        return False
    else:
        return True


def get_dimensions(matrix):
    rows = len(matrix.split('n'))
    columns = len(matrix.split('n')[0].split())

    return rows, columns


if __name__ == "__main__":
    app.run(port=5000)
