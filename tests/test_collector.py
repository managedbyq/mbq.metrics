from unittest import TestCase

from mbq import metrics
from tests.compat import mock


@mock.patch('mbq.metrics._statsd')
class CollectorTests(TestCase):

    def test_combine_metric(self, _statsd):
        collector = metrics.Collector(prefix='test1')
        with self.assertRaises(ValueError):
            collector._combine_metric('test2'),

        collector = metrics.Collector(namespace='namespace', prefix='test1')
        self.assertEqual(
            collector._combine_metric('test2'),
            'namespace.test1.test2',
        )
        with self.assertRaises(ValueError):
            collector._combine_metric(None),

        collector = metrics.Collector(namespace='namespace')
        self.assertEqual(
            collector._combine_metric('test2'),
            'namespace.test2',
        )

        with mock.patch('mbq.metrics._namespace', 'default_namespace'):
            collector = metrics.Collector(namespace='namespace', prefix='test1')
            self.assertEqual(
                collector._combine_metric('test2'),
                'namespace.test1.test2',
            )
            collector = metrics.Collector(prefix='test1')
            self.assertEqual(
                collector._combine_metric('test2'),
                'default_namespace.test1.test2',
            )

    @mock.patch('mbq.metrics._constant_tags', {'a': 1, 'b': 1})
    def test_combine_tags(self, _statsd):
        # uses constant tags only
        self.assertEqual(
            metrics.Collector()._combine_tags(None),
            ['a:1', 'b:1'],
        )

        # collector tags override constant_tags
        collector = metrics.Collector(tags={'a': '2', 'c': 1})
        self.assertEqual(
            collector._combine_tags(None),
            ['a:2', 'b:1', 'c:1'],
        )

        # event tags override collector tags
        self.assertEqual(
            collector._combine_tags({'a': '3', 'd': 1}),
            ['a:3', 'b:1', 'c:1', 'd:1'],
        )

    @mock.patch('mbq.metrics._namespace', 'constant_namespace')
    def test_service_check_name_and_tags(self, _statsd):
        collector = metrics.Collector(
            prefix='prefix',
            namespace='namespace',
            tags={'constant': 1, 't': 1},
        )
        collector.service_check('service_name', 1, tags={'t': 2})

        _statsd.service_check.assert_called_with(
            'namespace.prefix.service_name',
            1,
            tags=['constant:1', 't:2'],
            message=None,
        )

    def test_event_title_and_tags(self, _statsd):
        collector = metrics.Collector(
            namespace='app_namespace',
            prefix='prefix',
            tags={'tag': 'collector_tag'},
        )
        collector.event('event', 'hi!', tags={'tag': 'event_tag'})

        _statsd.event.assert_called_with(
            'app_namespace.prefix.event',
            'hi!',
            alert_type=None,
            source_type_name='my apps',
            tags=['tag:event_tag']
        )
