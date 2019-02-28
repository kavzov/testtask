import unittest
from task_4_get_queries import TestTaskHTTPRequestHandler


class TestTask4(unittest.TestCase):
    def setUp(self):
        self.obj = TestTaskHTTPRequestHandler(self, ('', 8080))

    def test_path(self):
        good_path = '/cats'
        bad_path = '/dogs'
        self.assertEqual([], self.obj.check_query_errors(good_path, []))
        self.assertIn('invalid path', self.obj.check_query_errors(bad_path, [])[0])
