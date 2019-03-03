import unittest
from task_5_post_query import PostQuery


class TestPostQuery(unittest.TestCase):
    def setUp(self):
        self.obj = PostQuery()
        self.valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        self.valid_colors = ['black', 'white', 'black & white', 'red', 'red & white', 'red & black & white']
        self.valid_query = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'

    def assertInvalid(self, invalid_query, error_msg):
        return self.assertIn(error_msg, self.obj.check(invalid_query, self.valid_attr_names, self.valid_colors)['error'])

    def test_json(self):
        valid_json = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length": 20}'
        invalid_json = '{"name": , "color": "black", "tail_length": 15, "whiskers_length": 20}'
        self.assertTrue(self.obj.check(valid_json, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertInvalid(invalid_json, 'invalid JSON')

    def test_attrs(self):
        invalid_attrs = '{"name": "Barsik", "color": "black", "weight": 7, "whiskers_length": 20}'
        self.assertInvalid(invalid_attrs, 'invalid attributes')

    def test_name(self):
        invalid_name = '{"name": "123", "color": "black", "tail_length": 15, "whiskers_length": 20}'
        namesake = ('Tihon',)
        self.assertInvalid(invalid_name, 'invalid name')
        self.assertIn('already exist', self.obj.check_namesake(namesake))
        self.assertIsNone(self.obj.check_namesake(None))

    def test_color(self):
        invalid_color = '{"name": "Barsik", "color": "orange", "tail_length": 15, "whiskers_length": 20}'
        self.assertIn('invalid color', self.obj.check(invalid_color, self.valid_attr_names, self.valid_colors)['error'])

    def test_tail_length(self):
        invalid_tail_length_str = '{"name": "Barsik", "color": "black", "tail_length": "eleven", "whiskers_length": 20}'
        invalid_tail_length_neg = '{"name": "Barsik", "color": "black", "tail_length": -10, "whiskers_length":20}'
        self.assertInvalid(invalid_tail_length_str, 'tail_length is not a number')
        self.assertInvalid(invalid_tail_length_neg, 'tail_length is not positive')

    def test_whiskers_length(self):
        invalid_whiskers_length_str = '{"name": "Barsik", "color": "black", "tail_length": 15, "whiskers_length": "ten"}'
        invalid_whiskers_length_neg = '{"name": "Barsik", "color": "black", "tail_length": 10, "whiskers_length": -20}'
        self.assertInvalid(invalid_whiskers_length_str, 'whiskers_length is not a number')
        self.assertInvalid(invalid_whiskers_length_neg, 'whiskers_length is not positive')
