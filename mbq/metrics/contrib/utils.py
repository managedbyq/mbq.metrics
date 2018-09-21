import re


DIGIT_ID_REGEX = re.compile(r'/[0-9]+')
UUID_REGEX = re.compile(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def _sluggified_path(path):
    path = re.sub(UUID_REGEX, '/:id', path)
    path = re.sub(DIGIT_ID_REGEX, '/:id', path)
    path = path[:-1] if path[-1] == '/' else path  # remove trailing '/' at end of urls
    return path


def get_response_metrics_tags(status_code, path, method):
    return {
        'path': _sluggified_path(path),
        'method': method,
        'status_code': status_code,
        'status_range': '{}xx'.format(status_code // 100),
    }
