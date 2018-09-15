import unittest
from urllib2 import urlopen


URLS = ['http://www.google.com', 'https://www.google.com']
TIMEOUT = 5


class HttpFirewallRulesTestCase(unittest.TestCase):

    def testHttpFirewallRules(self):
        responses = []
        for url in URLS:
            try:
                r = urlopen(url, timeout=TIMEOUT)
                responses.append(r)
            except Exception as e:
                responses.append(e)
                continue

        self.assertTrue(
                not any(
                    list(
                        map(lambda r: isinstance(r, (Exception,)), responses))))
        self.assertTrue(
                all(
                    list(
                        map(
                            lambda code: code < 400,
                            filter(
                                lambda r: not isinstance(r, (Exception,)),
                                responses)))))


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
