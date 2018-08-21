import re
from time import time

from mbq import metrics
from mbq.metrics.contrib import utils

DIGIT_ID_REGEX = re.compile('\/[0-9]+')
UUID_REGEX = re.compile('\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def _sluggified_path(path):
    return re.sub(DIGIT_ID_REGEX, '/:id', re.sub(UUID_REGEX, '/:id', path))


class TimingMiddleware(object):
    def __init__(self, app):
        self.app = app
        self.status_code = None

    def __call__(self, environ, start_response):
        """Meaure the time spent in the application."""
        start_time = time()

        def _start_response(status, headers, *args):
            self.status_code = int(status.split()[0])
            return start_response(status, headers, *args)

        response = self.app(environ, _start_response)

        tags = utils.compute_tags(
            self.status_code,
            environ.get('PATH_INFO', ''),
            environ.get('REQUEST_METHOD'),
        )

        metrics.increment('response', tags=tags)

        duration = time() - start_time
        duration_ms = int(round(duration * 1000))
        metrics.timing('request_duration_ms', duration_ms, tags=tags)

        return response
