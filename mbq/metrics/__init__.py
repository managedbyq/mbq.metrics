import functools
import logging

import datadog

from .__version__ import (  # noqa
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from . import utils

OK = datadog.DogStatsd.OK
WARNING = datadog.DogStatsd.WARNING
CRITICAL = datadog.DogStatsd.CRITICAL
UNKNOWN = datadog.DogStatsd.UNKNOWN

logger = logging.getLogger('mbq.metrics')

_constant_tags = {}
_initialized = False
_namespace = None
_statsd = datadog.DogStatsd(
    use_default_route=True,  # assumption: code is running in a container
)


def init(namespace=None, constant_tags=None):
    global _constant_tags, _initialized, _namespace
    if _initialized:
        logger.warning('mbq.metrics already initialized. Ignoring re-init.')
        return

    _constant_tags = constant_tags or {}
    _namespace = namespace
    _initialized = True


class Collector(object):
    def __init__(self, prefix=None, tags=None, namespace=None):
        self.prefix = prefix
        self._tags = tags or {}
        self._namespace = namespace

    def __call__(self, func):
        @functools.wraps(func)
        def wrapped(*args, **kwargs):
            args = list(args) + [self]
            try:
                return func(*args, **kwargs)
            finally:
                self.__exit__(None, None, None)

        return wrapped

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass

    @property
    def namespace(self):
        namespace = self._namespace or _namespace
        if not namespace:
            raise ValueError(
                'Collector must have a namespace. Either pass in a namespace to the constructor '
                'or call the mbq.metrics.init function to set a global default namespace.'
            )
        return namespace

    @property
    def tags(self):
        tags = _constant_tags.copy()
        tags.update(self._tags)
        return tags

    def _combine_metric(self, metric):
        if not metric:
            raise ValueError('Must include a metric name')

        combined_names = [self.namespace]

        if self.prefix:
            combined_names.append(self.prefix)

        combined_names.append(metric)

        return '.'.join(combined_names)

    def _combine_tags(self, tags):
        combined_tags = self.tags
        if tags:
            combined_tags.update(tags)
        return utils.tag_dict_to_list(combined_tags)

    def event(self, title, text, alert_type=None, tags=None):
        _statsd.event(
            self._combine_metric(title),
            text,
            alert_type=alert_type,
            tags=self._combine_tags(tags),
            source_type_name='my apps',
        )

    def gauge(self, metric, value, tags=None):
        _statsd.gauge(
            self._combine_metric(metric),
            value,
            tags=self._combine_tags(tags),
        )

    def increment(self, metric, value=1, tags=None):
        _statsd.increment(
            self._combine_metric(metric),
            value=value,
            tags=self._combine_tags(tags),
        )

    def timed(self, metric, tags=None, use_ms=None):
        return _statsd.timed(
            self._combine_metric(metric),
            tags=self._combine_tags(tags),
            use_ms=use_ms,
        )

    def timing(self, metric, value, tags=None):
        _statsd.timing(
            self._combine_metric(metric),
            value,
            tags=self._combine_tags(tags),
        )

    def service_check(self, check_name, status, tags=None, message=None):
        # the dogstatsd client doesn't use namespace or constant_tags
        # for service_check but we want to be consistent
        _statsd.service_check(
            self._combine_metric(check_name),
            status,
            tags=self._combine_tags(tags),
            message=message
        )


# expose as module-level functions
_default_collector = Collector()
event = _default_collector.event
gauge = _default_collector.gauge
increment = _default_collector.increment
timed = _default_collector.timed
timing = _default_collector.timing
service_check = _default_collector.service_check
