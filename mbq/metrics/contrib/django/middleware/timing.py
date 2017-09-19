from time import time

from django.conf import settings
try:
    from django.utils.deprecation import MiddlewareMixin as MiddlewareDeprecationMixin
except ImportError:
    MiddlewareDeprecationMixin = object

from mbq import metrics

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
        setattr(request, '_mbq-metrics-start-time', time())

    def process_response(self, request, response):

        if not hasattr(request, '_mbq-metrics-start-time'):
            return response

        duration = time() - getattr(request, '_mbq-metrics-start-time')
        duration_ms = int(round(duration * 1000))

        metrics.timing(
            'response-time',
            duration_ms,
            tags={
                'http-request-path': request.path,
                'http-request-method': request.method,
                'http-response-status': response.status_code,
                'http-response-length': len(response.content)
            }
        )

        return response
