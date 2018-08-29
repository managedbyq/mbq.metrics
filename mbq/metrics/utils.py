def tag_dict_to_list(tags):
    return sorted([
        ':'.join([str(k), str(v)]) if v else k
        for k, v in tags.items()
    ])


class MetricsError(Exception):
    pass


class NullStatsd:
    def __getattr__(self, attr):
        raise MetricsError('statsd has not been properly initialized')
