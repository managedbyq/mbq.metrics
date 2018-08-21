import re

DIGIT_ID_REGEX = re.compile('\/[0-9]+')
UUID_REGEX = re.compile('\/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}')


def _sluggified_path(path):
    return re.sub(DIGIT_ID_REGEX, '/:id', re.sub(UUID_REGEX, '/:id', path))


def compute_tags(status_code, path, method, content=None):
    return {
        'path': _sluggified_path(path),
        'method': method,
        'status_code': status_code,
        'status_range': '{}xx'.format(status_code // 100),
        'content_length': len(content) if content else None,
    }