# NOTE: Must be run as root

from scapy.all import *
import unittest
from util import getAddresses


GUEST_IP, _ = getAddresses('guest')
PORT = 5140
TIMEOUT = 1


class SyslogUdpFirewallRulesTestCase(unittest.TestCase):

    def testSyslog(self):
        ans = sr1(IP(dst=GUEST_IP)/UDP(dport=PORT,sport=54321)/Raw(load='hello'), timeout=TIMEOUT)
        self.assertIsNotNone(ans)
        self.assertEqual('world', ans[Raw].load)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
