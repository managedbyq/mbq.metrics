import unittest

from mbq import env, metrics
from tests.compat import mock


class GlobalTests(unittest.TestCase):

    def setUp(self):
        metrics._initialized = False

    @mock.patch('mbq.metrics._initialized', False)
    def test_init(self):
        metrics.init('service', env.Environment.LOCAL)
        self.assertTrue(metrics._initialized)

    @mock.patch('mbq.metrics._initialized', False)
    def test_constant_tags(self):
        metrics.init('service', env.Environment.LOCAL, constant_tags={
            'env': 'BAD',
            'another': 'GOOD',
        })
        self.assertEqual(set(metrics._constant_tags), {'env:local', 'another:GOOD'})

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
