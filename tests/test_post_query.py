import unittest
from task_5_post_query import POSTQuery
from settings import VALID_ATTR_NAMES, VALID_COLORS


class TestPostQuery(unittest.TestCase):

    VALID_QUERY = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length": 20}'

    def setUp(self):
        self.obj = POSTQuery()

    def assertInvalid(self, error_msg, invalid_query):
        return self.assertIn(error_msg, self.obj.check(invalid_query, VALID_ATTR_NAMES, VALID_COLORS)['error'])

    def test_json(self):
        invalid_json = '{"name": , "color": "black", "tail_length": 15, "whiskers_length": 20}'
        self.assertTrue(self.obj.check(self.VALID_QUERY, VALID_ATTR_NAMES, VALID_COLORS)['dict'])
        self.assertInvalid('invalid JSON', invalid_json)

    def test_attrs(self):
        invalid_attrs = '{"name": "Barsik", "color": "black", "weight": 7, "whiskers_length": 20}'
        self.assertInvalid('invalid attributes', invalid_attrs)

    def test_name(self):
        invalid_name = '{"name": "123", "color": "black", "tail_length": 15, "whiskers_length": 20}'
        namesake = ('Tihon',)
        self.assertInvalid('invalid name', invalid_name)
        self.assertIn('already exist', self.obj.check_namesake(namesake))
        self.assertIsNone(self.obj.check_namesake(None))

    def test_color(self):
        invalid_color = '{"name": "Barsik", "color": "orange", "tail_length": 15, "whiskers_length": 20}'
        self.assertInvalid('invalid color', invalid_color)

    def test_tail_length(self):
        invalid_tail_length_str = '{"name": "Barsik", "color": "black", "tail_length": "eleven", "whiskers_length": 20}'
        invalid_tail_length_neg = '{"name": "Barsik", "color": "black", "tail_length": -10, "whiskers_length": 20}'
        self.assertInvalid('tail_length is not a number', invalid_tail_length_str)
        self.assertInvalid('tail_length is not positive', invalid_tail_length_neg)

    def test_whiskers_length(self):
        invalid_whiskers_length_str = '{"name": "Barsik", "color": "black", "tail_length": 15, "whiskers_length": "ten"}'
        invalid_whiskers_length_neg = '{"name": "Barsik", "color": "black", "tail_length": 10, "whiskers_length": -20}'
        self.assertInvalid('whiskers_length is not a number', invalid_whiskers_length_str)
        self.assertInvalid('whiskers_length is not positive', invalid_whiskers_length_neg)
