import unittest

from mbq import metrics
from tests.compat import mock


class GlobalTests(unittest.TestCase):

    def setUp(self):
        metrics._initialized = False

    @mock.patch('mbq.metrics._initialized', False)
    def test_init(self):
        metrics.init()
        self.assertTrue(metrics._initialized)

    def test_global_functions_exist(self):
        methods = [
            'event',
            'gauge',
            'increment',
            'timed',
            'timing',
            'service_check'
        ]
        for method in methods:
            self.assertTrue(callable(getattr(metrics, method)))
