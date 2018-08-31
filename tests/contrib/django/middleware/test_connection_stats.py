# flake8: noqa
from unittest import TestCase

from .compat import mock, mock_open_patch

TEST_PROC_SYS_NET_IPV4_IP_LOCAL_PORT_RANGE = '30000	60000'

TEST_PROC_NET_TCP = '''  sl  local_address rem_address   st tx_queue rx_queue tr tm->when retrnsmt   uid  timeout inode
   0: 0B00007F:969B 00000000:0000 03 00000000:00000000 00:00000000 00000000     0        0 1038721 1 0000000000000000 100 0 0 10 0
   1: 00000000:18EB 00000000:0000 03 00000000:00000000 00:00000000 00000000   999        0 1041801 1 0000000000000000 100 0 0 10 0
   2: 0100007F:8774 0100007F:18EB 01 00000000:00000000 03:00001673 00000000     0        0 0 3 0000000000000000
   3: 0100007F:876E 0100007F:18EB 06 00000000:00000000 03:0000155E 00000000     0        0 0 3 0000000000000000
   4: 0100007F:18EB 0100007F:18EB 01 00000000:00000000 03:000015D6 00000000     0        0 0 3 0000000000000000
   5: 0100007F:18EB 0100007F:18EB 01 00000000:00000000 03:000015AD 00000000     0        0 0 3 0000000000000000'''


class ConnectionStatsMiddlewareTest(TestCase):
    @mock.patch('mbq.metrics.gauge')
    def test_middleware(self, mock_gauge):
        from mbq.metrics.contrib.django.middleware.connection_stats import ConnectionStatsMiddleware
        sut = ConnectionStatsMiddleware(mock.Mock())

        local_port_range_patch = mock_open_patch(TEST_PROC_SYS_NET_IPV4_IP_LOCAL_PORT_RANGE)
        local_port_range_patch.start()
        sut.local_port_range  # initialize local port range in lazy property
        local_port_range_patch.stop()

        proc_net_tcp_patch = mock_open_patch(TEST_PROC_NET_TCP)
        proc_net_tcp_patch.start()

        sut.report_metrics()
        mock_gauge.assert_has_calls([mock.call('connections', 2, {'state': 'active'}),
                                     mock.call('connections', 1, {'state': 'queued'})])
        proc_net_tcp_patch.stop()
