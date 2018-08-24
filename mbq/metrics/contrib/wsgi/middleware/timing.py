from time import time

from mbq import metrics
from mbq.metrics.contrib import utils


class TimingMiddleware(object):
    def __init__(self, app):
        self.app = app
        self.status_code = None

    def __call__(self, environ, start_response):
        start_time = time()

        def _start_response(status, headers, *args):
            self.status_code = int(status.split()[0])
            return start_response(status, headers, *args)

        response = self.app(environ, _start_response)

        tags = utils.get_response_metrics_tags(
            self.status_code,
            environ.get('PATH_INFO', ''),
            environ.get('REQUEST_METHOD'),
        )

        metrics.increment('response', tags=tags)

        duration = time() - start_time
        duration_ms = int(round(duration * 1000))
        metrics.timing('request_duration_ms', duration_ms, tags=tags)

        return response
