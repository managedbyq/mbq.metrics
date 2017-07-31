import functools
import logging

import datadog

from . import utils

OK = datadog.DogStatsd.OK
WARNING = datadog.DogStatsd.WARNING
CRITICAL = datadog.DogStatsd.CRITICAL
UNKNOWN = datadog.DogStatsd.UNKNOWN

logger = logging.getLogger('mbq.metrics')

_initialized = False
_statsd = utils.NullStatsd()


def init(namespace=None, constant_tags=None):
    global _initialized, _statsd
    if _initialized:
        logger.warning('mbq.metrics already initialized. Ignoring re-init.')
        return

    if constant_tags:
        constant_tags = utils.tag_dict_to_list(constant_tags)

    _statsd = datadog.DogStatsd(
        namespace=namespace,
        constant_tags=constant_tags,
        use_default_route=True,  # assumption: code is running in a container
    )
    _initialized = True


class Collector(object):
    def __init__(self, prefix=None, tags=None, statsd=None):
        self.prefix = prefix
        self.tags = tags or {}
        self._statsd = statsd

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
    def statsd(self):
        return self._statsd or _statsd

    def _combine_metric(self, metric):
        if not self.prefix:
            return metric

        return '.'.join([self.prefix, metric])

    def _combine_tags(self, tags):
        if not tags:
            tags = []
        elif isinstance(tags, dict):
            tags = utils.tag_dict_to_list(tags)

        return tags + utils.tag_dict_to_list(self.tags)

    def event(self, title, text, alert_type=None, tags=None):
        self.statsd.event(
            title,
            text,
            alert_type=alert_type,
            tags=self._combine_tags(tags),
            source_type_name='my apps',
        )

    def gauge(self, metric, value, tags=None):
        self.statsd.gauge(
            self._combine_metric(metric),
            value,
            tags=self._combine_tags(tags),
        )

    def increment(self, metric, value=1, tags=None):
        self.statsd.increment(
            self._combine_metric(metric),
            value=value,
            tags=self._combine_tags(tags),
        )

    def timed(self, metric, tags=None, use_ms=None):
        return self.statsd.timed(
            self._combine_metric(metric),
            tags=self._combine_tags(tags),
            use_ms=use_ms,
        )

    def timing(self, metric, value, tags=None):
        self.statsd.timing(
            self._combine_metric(metric),
            value,
            tags=self._combine_tags(tags),
        )

    def service_check(self, check_name, status, tags=None, message=None):
        # the dogstatsd client doesn't use namespace or constant_tags
        # for service_check but we want to be consistent

        check_name = self._combine_metric(check_name)
        if self.statsd.namespace:
            check_name = self.statsd.namespace + '.' + check_name

        tags = self._combine_tags(tags)
        if self.statsd.constant_tags:
            tags += self.statsd.constant_tags

        self.statsd.service_check(check_name, status, tags=tags, message=message)


# expose as module-level functions
_default_collector = Collector()
event = _default_collector.event
gauge = _default_collector.gauge
increment = _default_collector.increment
timed = _default_collector.timed
timing = _default_collector.timing
service_check = _default_collector.service_check
