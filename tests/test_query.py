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
        self.assertIn("invalid attribute", self.obj.check_query_errors('/cats', invalid_attrs)[0])

    def test_order(self):
        valid_order = {'order': ['desc']}
        invalid_order = {'order': ['misc']}
        invalid_order_multi = {'order': ['desc', 'asc']}
        self.assertEqual([], self.obj.check_query_errors('/cats', valid_order))
        self.assertIn("invalid order", self.obj.check_query_errors('/cats', invalid_order)[0])
        self.assertIn("'order' parameters given", self.obj.check_query_errors('/cats', invalid_order_multi)[0])

    def test_offset(self):
        # max_offset = Checker.get_dbtable_size('cats') - 1
        valid_offset = {'offset': ['10']}
        invalid_offset_sym = {'offset': ['ten']}
        invalid_offset_greater = {'offset': ['500']}
        invalid_offset_multi = {'offset': ['10', '20']}
        self.assertEqual([], self.obj.check_query_errors('/cats', valid_offset))
        self.assertIn("invalid offset", self.obj.check_query_errors('/cats', invalid_offset_sym)[0])
        self.assertIn("greater than allowed", self.obj.check_query_errors('/cats', invalid_offset_greater)[0])
        self.assertIn("'offset' parameters given", self.obj.check_query_errors('/cats', invalid_offset_multi)[0])

    def test_limit(self):
        valid_limit = {'limit': ['20']}
        invalid_limit = {'limit': ['twenty']}
        invalid_limit_multi = {'limit': ['20', '20']}
        self.assertEqual([], self.obj.check_query_errors('/cats', valid_limit))
        self.assertIn("invalid limit", self.obj.check_query_errors('/cats', invalid_limit)[0])
        self.assertIn("'limit' parameters given", self.obj.check_query_errors('/cats', invalid_limit_multi)[0])
