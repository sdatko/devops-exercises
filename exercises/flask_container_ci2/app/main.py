#!/usr/bin/env python3
# coding=utf-8

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
    return matrix.replace('', ' ').replace(' n ', '\n').strip()


@app.route("/columns/<matrix>/<column_number>", methods=['GET'])
def column(matrix, column_number):
    column_index = int(column_number) - 1
    return '\n'.join([row[column_index] for row in matrix.split('n')])


@app.route("/rows/<matrix>/<row_number>", methods=['GET'])
def row(matrix, row_number):
    row_index = int(row_number) - 1
    return matrix.split('n')[row_index].replace('', ' ').strip()


def pretty_json(arg):
    response = make_response(json.dumps(arg, sort_keys=True, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


if __name__ == "__main__":
    app.run(port=5000)
