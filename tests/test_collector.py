from unittest import TestCase

from mbq import metrics

from tests.compat import mock


class CollectorTests(TestCase):
    def test_combine_metric(self):
        collector = metrics.Collector(namespace='namespace', prefix='test1')
        self.assertEqual(
            collector._combine_metric('test2'),
            'namespace.test1.test2',
        )

    def test_combine_tags(self):
        collector = metrics.Collector(tags={'t': 1})
        self.assertEqual(
            collector._combine_tags({'t': 2}),
            ['t:2'],
        )
        self.assertEqual(
            collector._combine_tags(None),
            ['t:1'],
        )
        self.assertEqual(
            collector._combine_tags({'test': 2}),
            ['t:1', 'test:2'],
        )

    @mock.patch('mbq.metrics._is_initialized', return_value=False)
    @mock.patch('datadog.DogStatsd')
    def test_service_check_name_and_tags(self, DogStatsd, _is_initialized):
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

    @mock.patch('mbq.metrics._is_initialized', return_value=False)
    @mock.patch('datadog.DogStatsd')
    def test_event_title_and_tags(self, DogStatsd, _is_initialized):
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
