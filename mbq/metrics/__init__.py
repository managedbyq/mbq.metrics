import functools
import logging
import sys
from copy import copy

import datadog

import mbq.env

from . import utils
from .__version__ import (  # noqa
    __author__,
    __author_email__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)


OK = datadog.DogStatsd.OK
WARNING = datadog.DogStatsd.WARNING
CRITICAL = datadog.DogStatsd.CRITICAL
UNKNOWN = datadog.DogStatsd.UNKNOWN

logger = logging.getLogger('mbq.metrics')

_constant_tags: list
_initialized: bool = False
_service: str
_env: mbq.env.Environment
_statsd = datadog.DogStatsd(
    use_default_route=(sys.platform == "linux"),
)


def init(service: str, env: mbq.env.Environment, constant_tags=None):
    global _constant_tags, _initialized, _service, _env
    if _initialized:
        logger.warning('mbq.metrics already initialized. Ignoring re-init.')
        return

    _constant_tags = utils.tags_as_list(constant_tags)
    _service = service
    _env = env
    _initialized = True


class Collector(object):
    def __init__(self, prefix=None, tags=None, namespace=None):
        self.prefix = prefix
        self._tags = utils.tags_as_list(tags)
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
        namespace = self._namespace or _service
        if not namespace:
            raise ValueError(
                'Collector must have a namespace. Either pass in a namespace to the constructor '
                'or call the mbq.metrics.init function to set a global default namespace.'
            )
        return namespace

    def make_tags(self):
        tags = copy(_constant_tags)
        tags.extend(self._tags)
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
        combined_tags = self.make_tags()
        combined_tags.extend(utils.tags_as_list(tags))
        return combined_tags

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

    def histogram(self, metric, value, tags=None, sample_rate=1):
        _statsd.histogram(
            self._combine_metric(metric),
            value,
            tags=self._combine_tags(tags),
            sample_rate=sample_rate
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
