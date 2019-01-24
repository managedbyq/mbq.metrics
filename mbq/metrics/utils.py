def tags_as_list(tags) -> list:
    if tags is None:
        return []
    if isinstance(tags, (list, tuple)):
        return list(tags)
    elif isinstance(tags, dict):
        return sorted([
            ':'.join([str(k), str(v)]) if v else k
            for k, v in tags.items()
        ])
    raise ValueError('unexpected type for parameter tags')


class MetricsError(Exception):
    pass
