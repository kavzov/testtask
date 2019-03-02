import unittest
from task_4_get_queries import Query


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = Query()
        self.valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        self.valid_offset = 27

    def is_valid(self, query):
        valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        valid_offset = 27
        return self.obj.is_valid(query, valid_attr_names, valid_offset)

    def test_path(self):
        valid_path = '/cats?attribute=name'
        invalid_path = '/dogs?attribute=name'
        self.assertTrue(self.obj._valid_path(valid_path))
        self.assertFalse(self.obj._valid_path(invalid_path))

    def test_params(self):
        valid_params = ['attribute', 'limit']
        invalid_params = ['case', 'offset']
        self.assertTrue(self.obj._valid_params(valid_params))
        self.assertFalse(self.obj._valid_params(invalid_params))

    def test_attrs(self):
        valid_attrs = ['name', 'color']
        invalid_attrs = ['name', 'weight']
        self.assertTrue(self.obj._valid_attrs(valid_attrs, self.valid_attr_names))
        self.assertFalse(self.obj._valid_attrs(invalid_attrs, self.valid_attr_names))

    def test_order(self):
        valid_order = {'attribute': ['name'], 'order': ['desc']}
        invalid_order = {'attribute': ['name'], 'order': ['misc']}
        invalid_order_alone = {'order': ['desc']}
        invalid_order_multi = {'attribute': ['name'], 'order': ['asc', 'desc']}
        self.assertTrue(self.obj._valid_order(valid_order))
        self.assertFalse(self.obj._valid_order(invalid_order))
        self.assertFalse(self.obj._valid_order(invalid_order_alone))
        self.assertFalse(self.obj._valid_order(invalid_order_multi))

    def test_offset(self):
        valid_offset = ['10']
        invalid_offset_sym = ['ten']
        invalid_offset_greater = ['500']
        invalid_offset_multi = ['10', '20']
        self.assertTrue(self.obj._valid_offset(valid_offset, self.valid_offset))
        self.assertFalse(self.obj._valid_offset(invalid_offset_sym, self.valid_offset))
        self.assertFalse(self.obj._valid_offset(invalid_offset_greater, self.valid_offset))
        self.assertFalse(self.obj._valid_offset(invalid_offset_multi, self.valid_offset))

    def test_limit(self):
        valid_limit = ['20']
        invalid_limit = ['twenty']
        invalid_limit_multi = ['10', '20']
        self.assertTrue(self.obj._valid_limit(valid_limit))
        self.assertFalse(self.obj._valid_limit(invalid_limit))
        self.assertFalse(self.obj._valid_limit(invalid_limit_multi))

    def test_query(self):
        valid_query = '/cats?attribute=name&order=desc&offset=5&limit=10'
        invalid_query_path = '/dogs?attribute=name&order=desc&offset=5&limit=10'
        invalid_query_params = '/cats?case=name&order=desc&offset=5&limit=10'
        invalid_query_attr = '/cats?attribute=weight&order=desc&offset=5&limit=10'
        invalid_query_order_sym = '/cats?attribute=color&order=misc&offset=5&limit=10'
        invalid_query_order_alone = '/cats?order=desc&limit=10'
        invalid_query_order_multi = '/cats?attribute=color&order=asc&order=desc&limit=10'
        invalid_query_offset = '/cats?attribute=color&order=desc&offset=five&limit=10'
        invalid_query_offset_greater = '/cats?attribute=color&order=desc&offset=500&limit=10'
        invalid_query_offset_multi = '/cats?attribute=color&order=desc&&offset=25&offset=500'
        invalid_query_limit = '/cats?attribute=color&order=desc&offset=5&limit=ten'
        invalid_query_limit_multi = '/cats?attribute=color&order=desc&offset=5&limit=10&limit=20'
        self.assertTrue(self.is_valid(valid_query))
        self.assertFalse(self.is_valid(invalid_query_path))
        self.assertFalse(self.is_valid(invalid_query_params))
        self.assertFalse(self.is_valid(invalid_query_attr))
        self.assertFalse(self.is_valid(invalid_query_order_sym))
        self.assertFalse(self.is_valid(invalid_query_order_alone))
        self.assertFalse(self.is_valid(invalid_query_order_multi))
        self.assertFalse(self.is_valid(invalid_query_offset))
        self.assertFalse(self.is_valid(invalid_query_offset_greater))
        self.assertFalse(self.is_valid(invalid_query_offset_multi))
        self.assertFalse(self.is_valid(invalid_query_limit))
        self.assertFalse(self.is_valid(invalid_query_limit_multi))
