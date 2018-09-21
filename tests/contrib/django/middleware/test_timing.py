from unittest import TestCase

from compat import mock


class TimingMiddlewareTest(TestCase):

    def test_sluggified_path_no_transforms(self):
        from mbq.metrics.contrib.utils import _sluggified_path
        self.assertEqual(_sluggified_path('/i/am/a/path'), '/i/am/a/path')

    def test_sluggified_path_int_transforms(self):
        from mbq.metrics.contrib.utils import _sluggified_path
        self.assertEqual(_sluggified_path('/i/am/239847298374/path'), '/i/am/:id/path')

    def test_sluggified_path_removes_trailing_slash(self):
        from mbq.metrics.contrib.utils import _sluggified_path
        self.assertEqual(_sluggified_path('/i/am/239847298374/path/'), '/i/am/:id/path')

    def test_sluggified_path_doesnt_remove_only_slash(self):
        from mbq.metrics.contrib.utils import _sluggified_path
        self.assertEqual(_sluggified_path('/'), '/')

    def test_sluggified_path_uuid_and_int_transforms(self):
        from mbq.metrics.contrib.utils import _sluggified_path
        self.assertEqual(
            _sluggified_path('/i/am/88aa6219-9661-48fa-973a-6c60bbed1134/path/2394723948'),
            '/i/am/:id/path/:id')

    @mock.patch('mbq.metrics')
    @mock.patch('django.conf.settings')
    @mock.patch('time.time')
    def test_django_middleware(self, time, settings, metrics):
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
        }
        metrics.increment.assert_called_once_with('response', tags=tags)
        metrics.timing.assert_called_once_with('request_duration_ms', 1000, tags=tags)

    @mock.patch('mbq.metrics')
    @mock.patch('time.time')
    def test_wsgi_middleware_for_post_1_10(self, time, metrics):
        from mbq.metrics.contrib.wsgi.middleware.timing import TimingMiddleware

        time.side_effect = [1, 2]
        response_mock = mock.Mock()

        mock_environ = {
            'PATH_INFO': 'test/path/123',
            'REQUEST_METHOD': 'POST',
        }

        class App(object):
            def __call__(self, environ, start_response):
                start_response('400 NOT FOUND', {})
                return response_mock

        timing_middleware = TimingMiddleware(App())
        response = timing_middleware(mock_environ, lambda env, resp: response_mock)

        self.assertEqual(response, response_mock)

        tags = {
            'path': 'test/path/:id',
            'method': 'POST',
            'status_code': 400,
            'status_range': '4xx',
        }
        metrics.increment.assert_called_once_with('response', tags=tags)
        metrics.timing.assert_called_once_with('request_duration_ms', 1000, tags=tags)
