import unittest

from mbq import metrics

from mbq.metrics import utils

from tests.compat import mock


class GlobalTests(unittest.TestCase):

    def setUp(self):
        metrics._initialized = False
        metrics._statsd = utils.NullStatsd()

    @mock.patch('datadog.DogStatsd')
    def test_init(self, DogStatsd):
        metrics.init()
        self.assertTrue(DogStatsd.called)
        self.assertTrue(metrics._initialized)
        self.assertNotIsInstance(metrics._statsd, utils.NullStatsd)

    @mock.patch('datadog.DogStatsd')
    def test_create_statsd(self, DogStatsd):
        expected_returned_statsd = mock.Mock()
        DogStatsd.return_value = expected_returned_statsd
        statsd = metrics.create_statsd(
            namespace='test_namespace',
            constant_tags={'test': 'tags', 'one': 'two'},
        )
        DogStatsd.assert_called_with(
            namespace='test_namespace',
            constant_tags=['test:tags', 'one:two'],
            use_default_route=True,
        )
        self.assertEquals(statsd, expected_returned_statsd)

    @mock.patch('datadog.DogStatsd')
    def test_default_collector(self, DogStatsd):
        metrics.init()
        self.assertNotIsInstance(metrics._default_collector.statsd, utils.NullStatsd)

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
