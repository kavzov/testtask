import unittest
from task_4_get_queries import Checker


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = Checker()

    def test_path(self):
        good_path = '/cats'
        bad_path = '/dogs'
        self.assertEqual([], self.obj.check_query_errors(good_path, {}))
        self.assertIn('invalid path', self.obj.check_query_errors(bad_path, {})[0])

    def test_query_params(self):
        valid_params = {'attribute': []}
        invalid_params = {'case': []}
        self.assertEqual([], self.obj.check_query_errors('/cats', valid_params))
        self.assertIn('invalid query', self.obj.check_query_errors('/cats', invalid_params)[0])

    def test_attrs(self):
        valid_attrs = {'attribute': ['color', 'name']}
        invalid_attrs = {'attribute': ['id', 'length']}
        self.assertEqual([], self.obj.check_query_errors('/cats', valid_attrs))
        self.assertIn('invalid attribute', self.obj.check_query_errors('/cats', invalid_attrs)[0])

