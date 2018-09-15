# NOTE: Must be run as root.
# NOTE: Only the SYN flag should be set for the TCP packets most of the
#       other flag combinations a blocked by the firewall.
# Test that the following tcp ports are opened by the firewall:
#   * AyeAye, 4000
#   * Oxpecker, 5000
#   * PostgreSQL, 5432
#   * InfluxDB, 8086

from scapy.all import *
import unittest
from util import getAddresses


GUEST_IP, _ = getAddresses('guest')
PORTS = [5432, 8086]
WIN_RDP_PORT = 3389
TIMEOUT = 1


class TcpPortFirewallRulesTestCase(unittest.TestCase):

    def testTcpPorts(self):
        ps = [p for p in IP(dst=GUEST_IP)/TCP(flags='S', dport=PORTS)]
        for p in ps:
            ans = sr1(p, timeout=TIMEOUT)
            self.assertIsNotNone(ans)
            self.assertEqual(GUEST_IP, ans[IP].src)


    def testDressAsWindows(self):
        ans = sr1(
                IP(dst=GUEST_IP)/TCP(flags='S', dport=WIN_RDP_PORT),
                timeout=TIMEOUT)
        self.assertIsNotNone(ans)
        self.assertTrue(ICMP in ans)
        self.assertEqual(3, ans[ICMP].type)
        self.assertEqual(10, ans[ICMP].code)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
