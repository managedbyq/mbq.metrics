from unittest import TestCase

from mbq import metrics

from tests.compat import mock


class CollectorTests(TestCase):
    def test_combine_metric(self):
        collector = metrics.Collector(prefix='test1')
        self.assertEqual(
            collector._combine_metric('test2'),
            'test1.test2',
        )

    def test_combine_tags(self):
        collector = metrics.Collector(tags={'t': 1})
        self.assertEqual(
            collector._combine_tags({'t': 2}),
            ['t:2', 't:1'],
        )
        self.assertEqual(
            collector._combine_tags(None),
            ['t:1'],
        )
        self.assertEqual(
            collector._combine_tags(['test']),
            ['test', 't:1'],
        )

    def test_service_check_name_and_tags(self):
        statsd = mock.MagicMock()
        statsd.namespace = 'namespace'
        statsd.constant_tags = ['constant:1']

        collector = metrics.Collector(prefix='prefix', tags={'t': 1}, statsd=statsd)
        collector.service_check('service_name', 1, tags={'t': 2})

        statsd.service_check.assert_called_with(
            'namespace.prefix.service_name',
            1,
            tags=['t:2', 't:1', 'constant:1'],
            message=None,
        )
