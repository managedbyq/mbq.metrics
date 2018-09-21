import re


DIGIT_ID_REGEX = re.compile(r'/[0-9]+')
UUID_REGEX = re.compile(r'/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def _sluggified_path(path):
    path = re.sub(UUID_REGEX, '/:id', path)
    path = re.sub(DIGIT_ID_REGEX, '/:id', path)

    # Remove trailing '/' at end of urls, but only if path isn't "/"
    if path != '/' and path[-1] == '/':
        path = path[:-1]

    return path


def get_response_metrics_tags(status_code, path, method):
    return {
        'path': _sluggified_path(path),
        'method': method,
        'status_code': status_code,
        'status_range': '{}xx'.format(status_code // 100),
    }
