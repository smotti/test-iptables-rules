import re
from subprocess import CalledProcessError, check_output
import unittest
from util import parsePingOutput


def getGatewayAddr():
    routes = check_output('route -n', shell=True, universal_newlines=True)
    default =  routes.split('\n')[2] 
    return re.split('\s+', default)[1]


IFACE = 'eth1'
PKTS = 5
TIMEOUT = 5
DST = getGatewayAddr()
CMD = 'ping -c {} -W {} -I {} {}'.format(PKTS, TIMEOUT, IFACE, DST)


class IcmpFirewallRulesGuestTestCase(unittest.TestCase):

    def testInOutEcho(self):
        try:
            result = check_output(CMD, shell=True, universal_newlines=True)
        except CalledProcessError as e:
            self.fail(str(e))
        else:
            stats = parsePingOutput(result)
            self.assertTrue('tx' in stats)
            self.assertTrue('rx' in stats)
            self.assertEqual(PKTS, int(stats['tx']))
            # A delta of 4 considers potential network problems during test
            # that could lead to packet drops, thus if we receive at least
            # one reply we know the firewall rule forwards incoming icmp
            # replys.
            self.assertAlmostEqual(PKTS, int(stats['rx']), delta=4)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
