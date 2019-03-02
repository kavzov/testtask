import unittest
from task_4_get_queries import Query


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = Query()

    def is_valid(self, query):
        valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        valid_offset = 27
        return self.obj.is_valid(query, valid_attr_names, valid_offset)

    def test_query(self):
        valid_query = '/cats?attribute=name&order=desc&offset=5&limit=10'
        invalid_query_path = '/dogs?attribute=name&order=desc&offset=5&limit=10'
        invalid_query_params = '/cats?case=name&order=desc&offset=5&limit=10'
        invalid_query_attr = '/cats?attribute=weight&order=desc&offset=5&limit=10'
        invalid_query_order = '/cats?attribute=color&order=misc&offset=5&limit=10'
        invalid_query_order_alone = '/cats?order=desc&limit=10'
        invalid_query_order_multi = '/cats?attribute=color&order=asc&order=desc&limit=10'
        invalid_query_offset_sym = '/cats?attribute=color&order=desc&offset=five&limit=10'
        invalid_query_offset_greater = '/cats?attribute=color&order=desc&offset=500&limit=10'
        invalid_query_offset_multi = '/cats?attribute=color&order=desc&&offset=25&offset=500'
        invalid_query_limit_sym = '/cats?attribute=color&order=desc&offset=5&limit=ten'
        invalid_query_limit_multi = '/cats?attribute=color&order=desc&offset=5&limit=10&limit=20'
        self.assertTrue(self.is_valid(valid_query))
        self.assertFalse(self.is_valid(invalid_query_path))
        self.assertFalse(self.is_valid(invalid_query_params))
        self.assertFalse(self.is_valid(invalid_query_attr))
        self.assertFalse(self.is_valid(invalid_query_order))
        self.assertFalse(self.is_valid(invalid_query_order_alone))
        self.assertFalse(self.is_valid(invalid_query_order_multi))
        self.assertFalse(self.is_valid(invalid_query_offset_sym))
        self.assertFalse(self.is_valid(invalid_query_offset_greater))
        self.assertFalse(self.is_valid(invalid_query_offset_multi))
        self.assertFalse(self.is_valid(invalid_query_limit_sym))
        self.assertFalse(self.is_valid(invalid_query_limit_multi))
