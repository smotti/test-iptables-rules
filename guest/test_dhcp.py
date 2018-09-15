# NOTE: I think it's advisable to stop dhclient before running the test. Or
#       else the dhclient will accept the new lease.
# NOTE: It might also be necessary to disable eth0
# NOTE: This test is not accurate because scapy uses raw sockets, which
#       are not affected by iptable rules. But a test with dhclient still
#       confirmed that the rules are working properly.
from scapy.all import *
from socket import AF_INET, IPPROTO_UDP, socket, SOCK_DGRAM, SOL_SOCKET, \
    SO_BROADCAST
import unittest


conf.iface = 'eth1'


class DhcpFirewallRulesTestCase(unittest.TestCase):

    def setUp(self):
        _, self.rawmac = get_if_raw_hwaddr(conf.iface)
        self.mac = get_if_hwaddr(conf.iface)

        self.socket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
        self.socket.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
        self.socket.bind(('', 68))


    def tearDown(self):
        self.socket.close()


    def testDhcpViaDiscoverMessage(self):
        bootp = BOOTP(chaddr=self.rawmac)
        dhcp = DHCP(options=[('message-type', 'discover'), 'end'])
        dhcpDiscover = bootp/dhcp
        sent = self.socket.sendto(dhcpDiscover.build(), ('255.255.255.255', 67))

        # We use scapy here because, I don't know why we don't receive the
        # reply via the socket we created to send the dhcp discover.
        ans = sniff(
                iface=conf.iface,
                filter='udp and port 68 and ether dst {}'.format(self.mac),
                count=1)[0]

        self.assertTrue(BOOTP in ans)
        self.assertTrue(DHCP in ans)
        self.assertTrue(ans[BOOTP].op == 2)
        self.assertTrue(ans[DHCP].options[0][1] == 2)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
