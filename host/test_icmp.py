# NOTE: Requires root priviledges to run, because a ping interval below
#       1 seconds requires this. Another reason for root is the use of scapy.
from scapy.all import *
import unittest
from util import getAddresses


GUEST_IP, _ = getAddresses('guest')
PING_INTERVAL = 0.1
PKTS = 10
PKTS_RX = 9
ICMP_TYPES = [9, 10, 13, 15, 17]


class IcmpFirewallRulesHostTestCase(unittest.TestCase):

    def testRateLimiting(self):
        ans, unans = srloop(
                IP(dst=GUEST_IP)/ICMP(), inter=PING_INTERVAL, count=PKTS,
                verbose=0)
        self.assertTrue(PKTS_RX, len(ans))
        self.assertTrue(PKTS - PKTS_RX, len(unans))


    def testDropOfNotEchoRequests(self):
        ipPkt = IP(dst=GUEST_IP)
        icmpPkt = ICMP(type=ICMP_TYPES)
        pkts = [p for p in ipPkt/icmpPkt]

        rs = []
        for p in pkts:
            rs.append(sr1(p, timeout=1, verbose=0))
        self.assertTrue(all(list(map(lambda r: r is None, rs))))


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
