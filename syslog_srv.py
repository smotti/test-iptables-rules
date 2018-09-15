# NOTE: It justs receives a packet on a desired udp port and send back one
#       packet. Thus it's just for testing.

from socket import AF_INET, IPPROTO_UDP, SOCK_DGRAM, SOL_SOCKET, SO_REUSEADDR, \
    socket
from sys import exit
from util import getAddresses


PORT = 5140


if __name__ == '__main__':
    s = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    try:
        s.bind(('', PORT))
    except Exception as e:
        print('SYSLOG: Exception: ' + str(e))

    try:
        while True:
            msg, addr = s.recvfrom(1024)
            s.sendto('world', addr)
            break
    except KeyboardInterrupt as e:
        print('SYSLOG: Stop server')
        exit(0)
    except Exception as e:
        print('SYSLOG: Exception: ' + str(e))
        exit(1)
    else:
        s.close()
        print('SYSLOG: Stop server')
        exit(0)
    finally:
        s.close()
