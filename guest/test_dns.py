from scapy.all import *
from socket import AF_INET, IPPROTO_UDP, socket, SOCK_DGRAM
import unittest


conf.iface = 'eth1'

NAMESERVER = '8.8.8.8'


class DnsFirewallRulesTestCase(unittest.TestCase):

    def setUp(self):
        self.ipAddr = get_if_addr(conf.iface)
        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        # NOTE: The port is randomly choosen and must be in the range of the
        # linux ephemeral port range, which is: 32768 - 61000.
        self.socket.bind((self.ipAddr, 56789))
        self.socket.connect((NAMESERVER, 53))


    def tearDown(self):
        self.socket.close()


    def testDnsRules(self):
        dnsQuery = DNS(rd=1, qd=DNSQR(qname='www.medicustek.com'))
        sent = self.socket.send(dnsQuery.build())
        ans = DNS(self.socket.recv(4096))

        self.assertTrue(len(dnsQuery) == sent)
        self.assertTrue(len(ans) > 0)
        self.assertTrue(DNSRR in ans[DNS])


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
