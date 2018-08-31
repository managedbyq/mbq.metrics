from datetime import datetime, timedelta
import logging

from django.conf import settings

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

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if datetime.now() > LAST_REPORT + REPORTING_INTERVAL:
            LAST_REPORT = datetime.now()
            try:
                self.report_metrics()
            except Exception:
                logger.exception('Exception while trying to report connection queue metrics')

        response = self.get_response(request)
        return response

    def report_metrics(self):
        established_connections, waiting_connections = 0, 0
        with open('/proc/net/tcp', 'r') as f:
            for line in f.read().splitlines()[1:]:
                state_int = int(line.strip().split(' ')[3], 16)
                if state_int == ESTABLISHED_STATE:
                    established_connections += 1
                elif state_int == SYN_RECV_STATE:
                    waiting_connections += 1

        metrics.gauge('connections', established_connections, { 'state': 'active' })
        metrics.gauge('connections', waiting_connections, { 'state': 'queued' })
