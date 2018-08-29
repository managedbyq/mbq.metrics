from unittest import TestCase

from mbq import metrics

from tests.compat import mock


@mock.patch('mbq.metrics._initialized', False)
@mock.patch('datadog.DogStatsd')
class CollectorTests(TestCase):

    @mock.patch('mbq.metrics._initialized', False)
    @mock.patch('datadog.DogStatsd')
    def setUp(self, DogStatsd):
        metrics.init()

    def test_combine_metric(self, DogStatsd):
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

        metrics.init(namespace='default_namespace')
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

    def test_combine_tags(self, DogStatsd):
        collector = metrics.Collector(tags={'t': 1, 'u': 2})
        self.assertEqual(
            collector._combine_tags({'t': 2}),
            ['t:2', 'u:2'],
        )
        self.assertEqual(
            collector._combine_tags(None),
            ['t:1', 'u:2'],
        )
        self.assertEqual(
            collector._combine_tags({'s': 2}),
            ['s:2', 't:1', 'u:2'],
        )

        metrics.init(constant_tags={'t': 0, 'v': 3})
        self.assertEqual(
            collector._combine_tags({'t': 2}),
            ['t:2', 'u:2', 'v:3'],
        )
        self.assertEqual(
            collector._combine_tags(None),
            ['t:1', 'u:2', 'v:3'],
        )
        self.assertEqual(
            collector._combine_tags({'s': 2, 'v': 4}),
            ['s:2', 't:1', 'u:2', 'v:4'],
        )

    def test_service_check_name_and_tags(self, DogStatsd):
        statsd = mock.Mock()
        DogStatsd.return_value = statsd
        metrics.init(namespace='constant_namespace')
        collector = metrics.Collector(
            prefix='prefix',
            namespace='namespace',
            tags={'constant': 1, 't': 1},
        )
        collector.service_check('service_name', 1, tags={'t': 2})

        statsd.service_check.assert_called_with(
            'namespace.prefix.service_name',
            1,
            tags=['constant:1', 't:2'],
            message=None,
        )

    def test_event_title_and_tags(self, DogStatsd):
        statsd = mock.Mock()
        DogStatsd.return_value = statsd
        metrics.init(namespace='app_namespace', constant_tags={'a': 1, 'tag': 'constant'})

        collector = metrics.Collector(prefix='prefix', tags={'tag': 'collector_tag'})
        collector.event('event', 'hi!', tags={'tag': 'event_tag'})

        statsd.event.assert_called_with(
            'app_namespace.prefix.event',
            'hi!',
            alert_type=None,
            source_type_name='my apps',
            tags=['a:1', 'tag:event_tag']
        )
