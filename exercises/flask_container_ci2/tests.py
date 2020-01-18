#!/usr/bin/env python3
# coding=utf-8

import unittest
from unittest import mock

from app import main


class TestApp(unittest.TestCase):

    def setUp(self):
        self.app = main.app.test_client()

    def test_main_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_matrix(self):
        response = self.app.get('/matrix/123n456n789')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('UTF-8'), '1 2 3\n4 5 6\n7 8 9')

    def test_matrix_bad_character(self):
        response = self.app.get('/matrix/123n456,789')
        self.assertEqual(response.status_code, 400)

    def test_matrix_bad_dimension(self):
        response = self.app.get('/matrix/123n456n7890')
        self.assertEqual(response.status_code, 400)

    def test_column(self):
        response = self.app.get('/columns/123n456n789/2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('UTF-8'), '2\n5\n8')

    def test_column_bad_character(self):
        response = self.app.get('/columns/123n456,789/2')
        self.assertEqual(response.status_code, 400)

    def test_column_bad_dimension(self):
        response = self.app.get('/columns/123n456n7890/2')
        self.assertEqual(response.status_code, 400)

    def test_column_numer_too_big(self):
        response = self.app.get('/columns/123n456n7890/10')
        self.assertEqual(response.status_code, 400)

    def test_column_numer_negative(self):
        response = self.app.get('/columns/123n456n7890/-7')
        self.assertEqual(response.status_code, 400)

    def test_column_numer_not_int(self):
        response = self.app.get('/columns/123n456n7890/4.5')
        self.assertEqual(response.status_code, 400)

    def test_row(self):
        response = self.app.get('/rows/123n456n789/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode('UTF-8'), '1 2 3')

    def test_row_bad_character(self):
        response = self.app.get('/rows/123n456,789/1')
        self.assertEqual(response.status_code, 400)

    def test_row_bad_dimension(self):
        response = self.app.get('/rows/123n456n7890/1')
        self.assertEqual(response.status_code, 400)

    def test_row_numer_too_big(self):
        response = self.app.get('/rows/123n456n7890/10')
        self.assertEqual(response.status_code, 400)

    def test_row_numer_negative(self):
        response = self.app.get('/rows/123n456n7890/-7')
        self.assertEqual(response.status_code, 400)

    def test_row_numer_not_int(self):
        response = self.app.get('/rows/123n456n7890/4.5')
        self.assertEqual(response.status_code, 400)


class TestUtils(unittest.TestCase):

    @mock.patch('app.main.make_response')
    def test_pretty_json(self, make_response):
        class FakeResponse():
            headers = dict()
        make_response.return_value = FakeResponse()

        data1 = {"c": {"f": "g", "d": "e"}, "a": "b"}
        data2 = ('{\n'
                 '    "a": "b",\n'
                 '    "c": {\n'
                 '        "d": "e",\n'
                 '        "f": "g"\n'
                 '    }\n'
                 '}')
        result = main.pretty_json(data1)

        make_response.assert_called_once_with(data2)
        self.assertEqual(result.headers['Content-type'], "application/json")

    def test_verify_characters(self):
        result = main.verify_characters('123n456n789')
        self.assertTrue(result)

        result = main.verify_characters('123n456n7890')
        self.assertTrue(result)

        result = main.verify_characters('123n456,789')
        self.assertFalse(result)

        result = main.verify_characters('123n456,7890')
        self.assertFalse(result)

    def test_verify_dimensions(self):
        result = main.verify_dimensions('123n456n789')
        self.assertTrue(result)

        result = main.verify_dimensions('12345n67890')
        self.assertTrue(result)

        result = main.verify_dimensions('12345,67890')
        self.assertTrue(result)

        result = main.verify_dimensions('123n456n7890')
        self.assertFalse(result)

        result = main.verify_dimensions('123n456,789')
        self.assertFalse(result)

    def test_get_dimensions(self):
        rows, columns = main.get_dimensions('123n456n789')
        self.assertEqual(rows, 3)
        self.assertEqual(columns, 3)

        rows, columns = main.get_dimensions('12345n67890')
        self.assertEqual(rows, 2)
        self.assertEqual(columns, 5)

        rows, columns = main.get_dimensions('123n456n7890')
        self.assertEqual(rows, 3)
        self.assertEqual(columns, 3)


if __name__ == '__main__':
    unittest.main(verbosity=2)
