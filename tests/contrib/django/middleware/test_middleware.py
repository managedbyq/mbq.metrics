from distutils.version import StrictVersion
from unittest import TestCase, skipIf

import django

from compat import mock


class TimingMiddlewareTest(TestCase):

    def test_sluggified_path_no_transforms(self):
        from mbq.metrics.contrib.django.middleware.timing import _sluggified_path
        self.assertEqual(_sluggified_path('/i/am/a/path'), '/i/am/a/path')

    def test_sluggified_path_int_transforms(self):
        from mbq.metrics.contrib.django.middleware.timing import _sluggified_path
        self.assertEqual(_sluggified_path('/i/am/239847298374/path'), '/i/am/:id/path')

    def test_sluggified_path_uuid_and_int_transforms(self):
        from mbq.metrics.contrib.django.middleware.timing import _sluggified_path
        self.assertEqual(
            _sluggified_path('/i/am/88aa6219-9661-48fa-973a-6c60bbed1134/path/2394723948'),
            '/i/am/:id/path/:id')

    @skipIf(StrictVersion(django.__version__) >= StrictVersion('1.10'), 'New Style Middleware')
    @mock.patch('mbq.metrics')
    @mock.patch('django.conf.settings')
    @mock.patch('time.time')
    def test_middleware_for_pre_1_10(self, time, settings, metrics):
        from mbq.metrics.contrib.django.middleware.timing import TimingMiddleware

        time.side_effect = [1, 2]

        request_mock = mock.Mock(path='test/path', method='POST')
        timing_middleware = TimingMiddleware()
        timing_middleware.process_request(request_mock)

        self.assertTrue(hasattr(request_mock, '_mbq_metrics_start_time'))
        response_mock = mock.MagicMock(status_code=200, content='test')
        timing_middleware.process_response(request_mock, response_mock)

        tags = {
            'path': 'test/path',
            'method': 'POST',
            'status_code': 200,
            'status_range': '2xx',
            'content_length': 4,
        }
        metrics.increment.assert_called_once_with('response', tags=tags)
        metrics.timing.assert_called_once_with('request_duration_ms', 1000, tags=tags)

    @skipIf(StrictVersion(django.__version__) < StrictVersion('1.10'), 'Old Style Middleware')
    @mock.patch('mbq.metrics')
    @mock.patch('django.conf.settings')
    @mock.patch('time.time')
    def test_middleware_for_post_1_10(self, time, settings, metrics):
        from mbq.metrics.contrib.django.middleware.timing import TimingMiddleware

        time.side_effect = [1, 2]

        get_response_mock = mock.Mock(
            name='response_callable',
            return_value=mock.Mock(
                name='Response',
                status_code=200,
                content='test'
            )
        )

        timing_middleware = TimingMiddleware(get_response=get_response_mock)
        timing_middleware(mock.Mock(path='test/path/123', method='POST'))

        tags = {
            'path': 'test/path/:id',
            'method': 'POST',
            'status_code': 200,
            'status_range': '2xx',
            'content_length': 4,
        }
        metrics.increment.assert_called_once_with('response', tags=tags)
        metrics.timing.assert_called_once_with('request_duration_ms', 1000, tags=tags)
