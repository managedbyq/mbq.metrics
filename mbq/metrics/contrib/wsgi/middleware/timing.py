from time import time

from mbq import metrics


class TimingMiddleware(object):
    def __init__(self, app):
        self.app = app
        self.status_code = None

    def __call__(self, environ, start_response):
        """Meaure the time spent in the application."""
        start_time = time()
        print(environ)

        def _start_response(status, headers, *args):
            self.status_code = int(status.split()[0])
            return start_response(status, headers, *args)

        response = self.app(environ, _start_response)

        tags = {
            'path': environ.get('PATH_INFO'),
            'method': environ.get('REQUEST_METHOD'),
            'status_code': self.status_code,
            'status_range': '{}xx'.format(self.status_code // 100),
        }
        metrics.increment('response', tags=tags)

        duration = time() - start_time
        duration_ms = int(round(duration * 1000))
        metrics.timing('request_duration_ms', duration_ms, tags=tags)

        return response
