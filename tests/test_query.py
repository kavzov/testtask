import unittest
from task_4_get_queries import Query


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = Query()

    def check(self, query):
        valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        valid_offset = 27
        return self.obj.check(query, valid_attr_names, valid_offset)

    def test_path(self):
        valid_path = '/cats?attribute=name'
        invalid_path = '/dogs?attribute=name'
        self.assertIsNone(self.check(valid_path))
        self.assertIn("invalid path", self.check(invalid_path))

    def test_query_params(self):
        valid_param = '/cats?attribute=name'
        invalid_param = '/cats?case=name'
        self.assertIsNone(self.check(valid_param))
        self.assertIn("invalid query parameter", self.check(invalid_param))

    def test_attrs(self):
        valid_attrs = '/cats?attribute=name&attribute=color'
        invalid_attrs = '/cats?attribute=weight&attribute=color'
        self.assertIsNone(self.check(valid_attrs))
        self.assertIn("invalid attribute", self.check(invalid_attrs))

    def test_order(self):
        valid_order = '/cats?attribute=name&order=desc'
        invalid_order = '/cats?attribute=color&order=misc'
        invalid_order_alone = '/cats?order=asc&offset=10'
        invalid_order_multi = '/cats?attribute=color&order=asc&order=desc'
        self.assertIsNone(self.check(valid_order))
        self.assertIn("invalid order", self.check(invalid_order))
        self.assertIn("only with sorting parameter", self.check(invalid_order_alone))
        self.assertIn("'order' parameters given", self.check(invalid_order_multi))

    def test_offset(self):
        valid_offset = '/cats?offset=10'
        invalid_offset_sym = '/cats?offset=ten'
        invalid_offset_greater = '/cats?offset=500'
        invalid_offset_multi = '/cats?offset=10&offset=20'
        self.assertIsNone(self.check(valid_offset))
        self.assertIn("invalid offset", self.check(invalid_offset_sym))
        self.assertIn("greater than the maximum", self.check(invalid_offset_greater))
        self.assertIn("'offset' parameters given", self.check(invalid_offset_multi))

    def test_limit(self):
        valid_limit = '/cats?limit=20'
        invalid_limit_sym = '/cats?limit=twenty'
        invalid_limit_multi = '/cats?limit=20&limit=40'
        self.assertIsNone(self.check(valid_limit))
        self.assertIn("invalid limit", self.check(invalid_limit_sym))
        self.assertIn("'limit' parameters given", self.check(invalid_limit_multi))
