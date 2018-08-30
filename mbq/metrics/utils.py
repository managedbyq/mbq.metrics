def tag_dict_to_list(tags):
    return sorted([
        ':'.join([str(k), str(v)]) if v else k
        for k, v in tags.items()
    ])


class MetricsError(Exception):
    pass
