import time

from django.conf import settings
try:
    import django.utils.deprecation.MiddlewareMixin as MiddlewareMixin
    MiddlewareDeprecationMixin = MiddlewareMixin
except ImportError:
    MiddlewareDeprecationMixin = object

import mbq.metrics as metrics

DEFAULT_SETTINGS = {
    'EXCLUDED_PATHS': []
}

SETTINGS = DEFAULT_SETTINGS.copy()
SETTINGS.update(
    getattr(settings, 'MBQ_METRICS', {})
)


class TimingMiddleware(MiddlewareDeprecationMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):

        if request.path in SETTINGS['EXCLUDED_PATHS']:
            return request

        setattr(request, 'mbq-metrics-start-time', time.time())
        return request

    def process_response(self, request, response):

        if not hasattr(request, 'mbq-metrics-start-time'):
            return response

        duration = time.time() - getattr(request, 'mbq-metrics-start-time')
        duration_ms = int(round(duration * 1000))

        metrics.timing(
            'response-time',
            duration_ms,
            tags={
                '{}-endpoint': request.path,
                'http-request-method': request.method,
                'http-response-status': response.status_code,
                'http-response-length': len(response.content)
            }
        )

        return response
