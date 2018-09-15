from os.path import join
from subprocess import CalledProcessError, check_output
import unittest
from util import parseCfeTestOutput


TESTS_DIR = '/var/cfengine/masterfiles/policies/roles/mantis/tests/'


class CommonPolicyTestCase(unittest.TestCase):

    def test_FirewallPolicy(self):
        cfeTests = [
                'va_file_edit_template__usr_local_bin_firewall',
                'va_file_copy_local__etc_systemd_system_firewall_service',
                'va_file_copy_local__etc_dhcp_dhclient_exit_hooks_d_firewall',
                'va_service_start_firewall',
                'va_service_restart_firewall'
                ]

        try:
            out = check_output(
                    'cf-agent -K {}'.format(
                        join(TESTS_DIR, 'test_firewall.cf')),
                    shell=True,
                    universal_newlines=True)
        except CalledProcessError as e:
            self.fail(str(e))
        else:
            testResult = parseCfeTestOutput(out)
            print('FAILED: ' + str(testResult['failed']))
            print('PASSED: ' + str(testResult['passed']))
            self.assertEqual(0, len(testResult['failed']))
            self.assertEqual(len(cfeTests), len(testResult['passed']))
            passed = list(map(lambda t: t in testResult['passed'], cfeTests))
            self.assertTrue(all(passed))


if __name__ == '__main__':
    import xmlrunner
    unittest.main(testRunner=xmlrunner.XMLTestRunner(output='test-reports'))
