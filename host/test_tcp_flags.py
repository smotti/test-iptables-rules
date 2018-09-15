# NOTE: Must be run as root


from scapy.all import *
import unittest
from util import getAddresses


GUEST_IP, _ = getAddresses('guest')
TEST_PORT = 5432
TIMEOUT = 1


class BadTcpFlagsFirewallRuleTestCase(unittest.TestCase):

    def setUp(self):
        self.allFlags = 'FSRPAUEC'
        self.merryXmas = 'FSRAUEC'
        self.xmas = 'FPU'
        self.stealthSF = 'SF'
        self.stealthSR = 'SR'
        self.finOnly = 'F'
        self.null = ''
        self.ackOnly = 'A'


    def test_PacketWithAllFlags_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.allFlags)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_MerryXmasPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.merryXmas)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_XmasPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.xmas)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_SynFinPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.stealthSF)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_SynRstPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.stealthSR)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_FinOnlyPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.finOnly)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_NoFlagsPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.null)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


    def test_AckOnlyPacket_Blocked(self):
        pkt = IP(dst=GUEST_IP)/TCP(dport=TEST_PORT, flags=self.ackOnly)
        ans = sr1(pkt, timeout=TIMEOUT)
        self.assertIsNone(ans)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
