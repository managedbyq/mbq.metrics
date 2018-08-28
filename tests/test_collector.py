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

    @mock.patch('datadog.DogStatsd')
    # @mock.patch('datadog.DogStatsd.service_check')
    def test_service_check_name_and_tags(self, DogStatsd):
        statsd = mock.Mock()
        DogStatsd.return_value = statsd
        metrics.init()
        collector = metrics.Collector(
            prefix='prefix',
            namespace='namespace',
            tags={'constant': 1, 't': 1},
        )
        collector.service_check('service_name', 1, tags={'t': 2})

        statsd.service_check.assert_called_with(
            'namespace.prefix.service_name',
            1,
            tags=['t:2', 't:1', 'constant:1'],
            message=None,
        )

    def test_event_title_and_tags(self):
        statsd = mock.MagicMock()
        statsd.namespace = 'app_namespace'

        collector = metrics.Collector(prefix='prefix', tags={'tag': 'collector_tag'}, statsd=statsd)
        collector.event('event', 'hi!', tags={'tag': 'event_tag'})

        statsd.event.assert_called_with(
            'app_namespace.prefix.event',
            'hi!',
            alert_type=None,
            source_type_name='my apps',
            tags=['tag:event_tag', 'tag:collector_tag']
        )
