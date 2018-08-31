from time import time

from django.conf import settings

from mbq import metrics
from mbq.metrics.contrib import utils


try:
    from django.utils.deprecation import MiddlewareMixin as MiddlewareDeprecationMixin
except ImportError:
    MiddlewareDeprecationMixin = object


SETTINGS = {
    'EXCLUDED_PATHS': set()
}
SETTINGS.update(
    getattr(settings, 'MBQ_METRICS', {})
)
SETTINGS['EXCLUDED_PATHS'] = {path.strip('/') for path in SETTINGS['EXCLUDED_PATHS']}


class TimingMiddleware(MiddlewareDeprecationMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        if request.path.strip('/') in SETTINGS['EXCLUDED_PATHS']:
            return request
        setattr(request, '_mbq_metrics_start_time', time())

    def process_response(self, request, response):

        tags = utils.get_response_metrics_tags(
            response.status_code,
            request.path,
            request.method,
        )

        metrics.increment('response', tags=tags)

        if hasattr(request, '_mbq_metrics_start_time'):
            duration = time() - request._mbq_metrics_start_time
            duration_ms = int(round(duration * 1000))
            metrics.timing('request_duration_ms', duration_ms, tags=tags)

        return response
