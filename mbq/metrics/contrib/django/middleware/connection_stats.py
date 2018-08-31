import logging
from collections import Counter
from datetime import datetime, timedelta

from mbq import metrics


# https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/include/net/tcp_states.h?id=HEAD
ESTABLISHED_STATE = 1
SYN_RECV_STATE = 3

REPORTING_INTERVAL = timedelta(seconds=10)
LAST_REPORT = datetime.now()

logger = logging.getLogger('mbq.metrics')


class ConnectionStatsMiddleware(object):
    """Middleware reporting a periodic gauge metric on how many connections
    are active or in the waiting state, i.e. have not yet been accepted by the
    web server process.

    This is based on the global /proc/net so it will give you inaccurate
    results if your application is not running in its own container.
    """
    _local_port_range = None

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        global LAST_REPORT
        if datetime.now() > LAST_REPORT + REPORTING_INTERVAL:
            LAST_REPORT = datetime.now()
            try:
                self.report_metrics()
            except Exception:
                logger.exception('Exception while trying to report connection queue metrics')

        response = self.get_response(request)
        return response

    @property
    def local_port_range(self):
        """Tuple of (low_port, high_port) reflecting the local port range
        assigned to outbound connections. We use this as part of a heuristic
        to determine whether a connection is inbound or outbound.
        """
        if self._local_port_range is None:
            with open('/proc/sys/net/ipv4/ip_local_port_range', 'r') as f:
                self._local_port_range = tuple(map(int, f.read().split('\t')))
        return self._local_port_range

    def report_metrics(self):
        with open('/proc/net/tcp', 'r') as f:
            local_low, local_high = self.local_port_range
            all_connections = [conn.strip().split(' ')
                               for conn in f.read().splitlines()[1:]]
            inbound_connections = [conn for conn in all_connections
                                   if not local_low <= int(conn[1].split(':')[1], 16) <= local_high]

        states = Counter(int(conn[3], 16) for conn in inbound_connections)

        metrics.gauge('connections', states[ESTABLISHED_STATE], {'state': 'active'})
        metrics.gauge('connections', states[SYN_RECV_STATE], {'state': 'queued'})
