import unittest
from task_4_get_queries import Query


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = Query()

    def validate(self, query):
        valid_attr_names = ['name', 'color', 'tail_length', 'whiskers_length']
        valid_offset = 27
        return self.obj.is_valid(query, valid_attr_names, valid_offset)

    def test_path(self):
        valid_path = '/cats'
        invalid_path = '/dogs'
        self.assertTrue(self.validate(valid_path))
        self.assertFalse(self.validate(invalid_path))

    def test_query_params(self):
        valid_param = '/cats?attribute=name'
        invalid_param = '/cats?case=name'
        self.assertTrue((self.validate(valid_param)))
        self.assertFalse((self.validate(invalid_param)))

    def test_attrs(self):
        valid_attrs = '/cats?attribute=name&attribute=color'
        invalid_attrs = '/cats?attribute=weight'
        self.assertTrue((self.validate(valid_attrs)))
        self.assertFalse((self.validate(invalid_attrs)))

    def test_order(self):
        valid_order = '/cats?attribute=name&order=desc'
        invalid_order = '/cats?attribute=color&order=misc'
        invalid_order_alone = '/cats?order=asc'
        invalid_order_multi = '/cats?attribute=color&order=asc&order=desc'
        self.assertTrue((self.validate(valid_order)))
        self.assertFalse((self.validate(invalid_order)))
        self.assertFalse((self.validate(invalid_order_alone)))
        self.assertFalse((self.validate(invalid_order_multi)))

    def test_offset(self):
        valid_offset = '/cats?offset=10'
        invalid_offset_sym = '/cats?offset=ten'
        invalid_offset_greater = '/cats?offset=500'
        invalid_offset_multi = '/cats?offset=10&offset=20'
        self.assertTrue((self.validate(valid_offset)))
        self.assertFalse((self.validate(invalid_offset_sym)))
        self.assertFalse((self.validate(invalid_offset_greater)))
        self.assertFalse((self.validate(invalid_offset_multi)))

    def test_limit(self):
        valid_limit = '/cats?limit=20'
        invalid_limit_sym = '/cats?limit=twenty'
        invalid_limit_multi = '/cats?limit=20&limit=40'
        self.assertTrue((self.validate(valid_limit)))
        self.assertFalse((self.validate(invalid_limit_sym)))
        self.assertFalse((self.validate(invalid_limit_multi)))
