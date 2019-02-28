import time

from django.conf import settings

from mbq.metrics.contrib.utils import collector, get_response_metrics_tags


try:
    from django.utils.deprecation import MiddlewareMixin as MiddlewareDeprecationMixin
except ImportError:
    MiddlewareDeprecationMixin = object


SETTINGS: dict = {
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
        setattr(request, '_mbq_metrics_start_time', time.monotonic())

    def process_response(self, request, response):

        tags = get_response_metrics_tags(
            response.status_code,
            request.path,
            request.method,
        )

        collector.increment('response', tags=tags)

        if hasattr(request, '_mbq_metrics_start_time'):
            duration = time.monotonic() - request._mbq_metrics_start_time
            duration_ms = int(round(duration * 1000))
            collector.timing('request_duration_ms', duration_ms, tags=tags)

        return response
