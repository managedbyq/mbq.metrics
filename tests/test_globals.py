import unittest

from mbq import metrics

from mbq.metrics import utils

from tests.compat import mock


class GlobalTests(unittest.TestCase):

    def setUp(self):
        metrics._initialized = False
        metrics._statsd = utils.NullStatsd()

    @mock.patch('mbq.metrics._initialized', False)
    @mock.patch('datadog.DogStatsd')
    def test_init(self, DogStatsd):
        metrics.init()
        self.assertTrue(DogStatsd.called)
        self.assertTrue(metrics._initialized)
        self.assertNotIsInstance(metrics._statsd, utils.NullStatsd)

    @mock.patch('mbq.metrics._initialized', False)
    @mock.patch('datadog.DogStatsd')
    def test_default_collector(self, DogStatsd):
        metrics.init()
        self.assertNotIsInstance(metrics._statsd, utils.NullStatsd)

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
