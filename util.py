from os.path import abspath, dirname, isfile, join
import re
from sys import exit


GUEST_IFACE_INFO = join(dirname(abspath(__file__)), 'guest_iface_info')
HOST_IFACE_INFO = join(dirname(abspath(__file__)), 'host_iface_info')


def getAddresses(who):
    if who == 'host':
        path = HOST_IFACE_INFO
    else:
        path = GUEST_IFACE_INFO

    if not isfile(path):
        print('No such file {}'.format(path))
        exit(1)
    else:
        with open(path, 'r') as f:
            l = f.read().strip()
        ip, mac = l.split(',')
        return ip, mac


def parsePingOutput(output):
    pktStats = output.split('\n')[-3]
    m = re.match('^(?P<tx>[\d]+) .*, (?P<rx>[\d]+) .*$', pktStats)
    if m is not None:
        return m.groupdict()
    else:
        return {}


def parseCfeTestOutput(output):
    parsed = {'passed': [], 'failed': []}
    for l in output.split('\n'):
        stripped = l.lstrip('R: ')
        if stripped.startswith('PASS: '):
            parsed['passed'].append(stripped.split('PASS: ')[-1])
        elif stripped.startswith('FAIL: '):
            parsed['failed'].append(stripped.split('FAIL: ')[-1])

    return parsed
