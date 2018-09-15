# NOTE: For this test to work you'll need to stop any other NTP clients.
from scapy.all import *
from socket import AF_INET, IPPROTO_UDP, SOCK_DGRAM, socket
import unittest
from util import getAddresses


IFACE = 'eth1'
HOST_IP, _ = getAddresses('host')


class NtpFirewallRulesTestCase(unittest.TestCase):

    def setUp(self):
        self.ipAddr = get_if_addr(IFACE)
        
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.socket.bind((self.ipAddr, 123))
        self.socket.connect((HOST_IP, 123))
        self.socket.settimeout(1)


    def tearDown(self):
        self.socket.close()


    def testInOutRules(self):
        pkt = NTP()
        
        try:
            sent = self.socket.send(pkt.build())
        except Exception as e:
            self.fail(str(e))

        try:
            reply = self.socket.recv(4096)
        except Exception as e:
            self.fail(str(e))

        self.assertTrue(sent, len(reply))


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
