import unittest
import json
from task_5_post_query import PostQuery


class TestPostQuery(unittest.TestCase):
    def setUp(self):
        self.obj = PostQuery()
        self.valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        self.valid_colors = ['black', 'white', 'black & white', 'red', 'red & white', 'red & black & white']

    def test_json(self):
        valid_json = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'
        invalid_json = '{"name": , "color": "black", "tail_length": 15, "whiskers_length":20}'
        self.assertTrue(self.obj.validate(valid_json, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertIn('invalid JSON', self.obj.validate(invalid_json, self.valid_attr_names, self.valid_colors)['error'])

    def test_attrs(self):
        valid_attrs = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'
        invalid_attrs = '{"name": "Barsik", "color": "black", "weight": 7, "whiskers_length":20}'
        self.assertTrue(self.obj.validate(valid_attrs, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertIn('invalid attributes', self.obj.validate(invalid_attrs, self.valid_attr_names, self.valid_colors)['error'])

    def test_name(self):
        valid_name = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'
        invalid_name = '{"name": "123", "color": "black", "tail_length": 15, "whiskers_length":20}'
        invalid_name_sake = '{"name": "Tihon", "color": "black", "tail_length": 15, "whiskers_length":20}'
        self.assertTrue(self.obj.validate(valid_name, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertIn('invalid name', self.obj.validate(invalid_name, self.valid_attr_names, self.valid_colors)['error'])
        self.assertIn('already exist', self.obj.check(json.loads(invalid_name_sake), True))

    def test_color(self):
        valid_color = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'
        invalid_color = '{"name": "Barsik", "color": "orange", "tail_length": 15, "whiskers_length":20}'
        self.assertTrue(self.obj.validate(valid_color, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertIn('invalid color', self.obj.validate(invalid_color, self.valid_attr_names, self.valid_colors)['error'])

    def test_tail_length(self):
        valid_tail_length = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'
        invalid_tail_length_str = '{"name": "Barsik", "color": "black", "tail_length": "eleven", "whiskers_length":20}'
        invalid_tail_length_neg = '{"name": "Barsik", "color": "black", "tail_length": -10, "whiskers_length":20}'
        self.assertTrue(self.obj.validate(valid_tail_length, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertIn('tail_length not a number', self.obj.validate(invalid_tail_length_str, self.valid_attr_names, self.valid_colors)['error'])
        self.assertIn('tail_length is not positive', self.obj.check(json.loads(invalid_tail_length_neg), False))

    def test_whiskers_length(self):
        valid_whiskers_length = '{"name": "Barsik", "color": "black", "tail_length": 11, "whiskers_length":20}'
        invalid_whiskers_length_str = '{"name": "Barsik", "color": "black", "tail_length": 15, "whiskers_length":"ten"}'
        invalid_whiskers_length_neg = '{"name": "Barsik", "color": "black", "tail_length": 10, "whiskers_length":-20}'
        self.assertTrue(self.obj.validate(valid_whiskers_length, self.valid_attr_names, self.valid_colors)['dict'])
        self.assertIn('whiskers_length not a number', self.obj.validate(invalid_whiskers_length_str, self.valid_attr_names, self.valid_colors)['error'])
        self.assertIn('whiskers_length is not positive', self.obj.check(json.loads(invalid_whiskers_length_neg), False))
