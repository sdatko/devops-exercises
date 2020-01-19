#!/usr/bin/env python3
# coding=utf-8

import os

import requests


APP_HOST = os.environ.get('APP_HOST', '127.0.0.1')
APP_PORT = os.environ.get('APP_PORT', '5000')
BASE_URL = 'http://{host}:{port}'.format(host=APP_HOST, port=APP_PORT)


def test_main_page():
    response = requests.get('{}/'.format(BASE_URL))

    assert response.status_code == 200
    assert response.headers.get('Content-type', '') == "application/json"
    assert 'resources' in response.json().keys()
    assert 'current_uri' in response.json().keys()
    assert 'example' in response.json().keys()


def test_matrix():
    response = requests.get('{}/matrix/123n456n789'.format(BASE_URL))

    assert response.status_code == 200
    assert response.content.decode('UTF-8') == '1 2 3\n4 5 6\n7 8 9'


def test_matrix_invalid():
    response = requests.get('{}/matrix/123n456,789'.format(BASE_URL))

    assert response.status_code == 400
    assert 'Invalid characters in matrix.' in response.content.decode('UTF-8')


def test_column():
    response = requests.get('{}/columns/123n456n789/2'.format(BASE_URL))

    assert response.status_code == 200
    assert response.content.decode('UTF-8') == '2\n5\n8'


def test_column_non_int():
    response = requests.get('{}/columns/123n456n789/7.5'.format(BASE_URL))

    assert response.status_code == 400
    assert 'Incorrect value given as column number.' \
           in response.content.decode('UTF-8')


def test_row():
    response = requests.get('{}/rows/123n456n789/1'.format(BASE_URL))

    assert response.status_code == 200
    assert response.content.decode('UTF-8')


def test_row_negative():
    response = requests.get('{}/rows/123n456n789/-1'.format(BASE_URL))

    assert response.status_code == 400
    assert 'Wrong row number requested.' in response.content.decode('UTF-8')
