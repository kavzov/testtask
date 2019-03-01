import unittest
from task_4_get_queries import Checker


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = Checker()
        self.obj.VALID_ATTR_VALUES = (lambda: ['name', 'color', 'tail_length', 'whiskers_length'])()

    def test_path(self):
        valid_path = '/cats'
        invalid_path = '/dogs'
        self.assertEqual([], self.obj.check_query(valid_path))
        self.assertIn('invalid path', self.obj.check_query(invalid_path)[0])

    def test_query_params(self):
        valid_param = '/cats?attribute=name'
        invalid_param = '/cats?case=name'
        self.assertEqual([], self.obj.check_query(valid_param))
        self.assertIn('invalid query', self.obj.check_query(invalid_param)[0])

    def test_attrs(self):
        valid_attrs = '/cats?attribute=name&attribute=color'
        invalid_attrs = '/cats?attribute=id'
        self.assertEqual([], self.obj.check_query(valid_attrs))
        self.assertIn("invalid attribute", self.obj.check_query(invalid_attrs)[0])

    def test_order(self):
        valid_order = '/cats?attribute=name&order=desc'
        invalid_order = '/cats?attribute=color&order=misc'
        invalid_order_single = '/cats?order=asc'
        invalid_order_multi = '/cats?attribute=color&order=asc&order=desc'
        self.assertEqual([], self.obj.check_query(valid_order))
        self.assertIn("invalid order", self.obj.check_query(invalid_order)[0])
        self.assertIn("only with sorting parameter", self.obj.check_query(invalid_order_single)[0])
        self.assertIn("'order' parameters given", self.obj.check_query(invalid_order_multi)[0])

    def test_offset(self):
        valid_offset = '/cats?offset=10'
        invalid_offset_sym = '/cats?offset=ten'
        invalid_offset_greater = '/cats?offset=500'
        invalid_offset_multi = '/cats?offset=10&offset=20'
        self.assertEqual([], self.obj.check_query(valid_offset))
        self.assertIn("invalid offset", self.obj.check_query(invalid_offset_sym)[0])
        self.assertIn("greater than allowed", self.obj.check_query(invalid_offset_greater)[0])
        self.assertIn("'offset' parameters given", self.obj.check_query(invalid_offset_multi)[0])

    def test_limit(self):
        valid_limit = '/cats?limit=20'
        invalid_limit = '/cats?limit=twenty'
        invalid_limit_multi = '/cats?limit=20&limit=40'
        self.assertEqual([], self.obj.check_query(valid_limit))
        self.assertIn("invalid limit", self.obj.check_query(invalid_limit)[0])
        self.assertIn("'limit' parameters given", self.obj.check_query(invalid_limit_multi)[0])
