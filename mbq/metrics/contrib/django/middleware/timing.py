import re
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

DIGIT_ID_REGEX = re.compile('\/[0-9]+')
UUID_REGEX = re.compile('\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def _sluggified_path(path):
    return re.sub(DIGIT_ID_REGEX, '/:id', re.sub(UUID_REGEX, '/:id', path))


class TimingMiddleware(MiddlewareDeprecationMixin):

    def __init__(self, get_response=None):
        self.get_response = get_response

    def process_request(self, request):
        if request.path.strip('/') in SETTINGS['EXCLUDED_PATHS']:
            return request
        setattr(request, '_mbq_metrics_start_time', time())

    def process_response(self, request, response):

        tags = {
            'path': _sluggified_path(request.path),
            'method': request.method,
            'status_code': response.status_code,
            'status_range': '{}xx'.format(response.status_code // 100),
            # streaming responses don't have a content attribute
            'content_length': len(response.content) if getattr(response, 'content', None) else None,
        }
        metrics.increment('response', tags=tags)

        if hasattr(request, '_mbq_metrics_start_time'):
            duration = time() - request._mbq_metrics_start_time
            duration_ms = int(round(duration * 1000))
            metrics.timing('request_duration_ms', duration_ms, tags=tags)

        return response
