from socket import AF_INET, IPPROTO_TCP, SOCK_STREAM, socket
import unittest
from util import getAddresses


HOST_IP, _ = getAddresses('host')


class SmtpFirewallRulesTestCase(unittest.TestCase):

    def setUp(self):
        self.s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
        self.port25 = 25
        self.port465 = 465
        self.port587 = 587
        self.msg = 'hello'
        self.answer = 'DUDE'


    def tearDown(self):
        self.s.shutdown(1)
        self.s.close()


    def testSmtpPort25(self):
        try:
            self.s.connect((HOST_IP, self.port25))
        except Exception as e:
            self.fail(str(e))

        sent = self.s.send(self.msg)
        self.assertEqual(len(self.msg), sent)

        answer = self.s.recv(1024)
        self.assertEqual(self.answer, answer)


    def testSmtpPort465(self):
        try:
            self.s.connect((HOST_IP, self.port465))
        except Exception as e:
            self.fail(str(e))

        sent = self.s.send(self.msg)
        self.assertEqual(len(self.msg), sent)

        answer = self.s.recv(1024)
        self.assertEqual(self.answer, answer)


    def testSmtpPort587(self):
        try:
            self.s.connect((HOST_IP, self.port587))
        except Exception as e:
            self.fail(str(e))

        sent = self.s.send(self.msg)
        self.assertEqual(len(self.msg), sent)

        answer = self.s.recv(1024)
        self.assertEqual(self.answer, answer)


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
