# NOTE: Must be run as root, in order to set the required iptables rule.
from netfilterqueue import NetfilterQueue
from scapy.all import *
from subprocess import CalledProcessError, check_call
from sys import exit
from util import getAddresses


GUEST_IP, _ = getAddresses('guest')
IPT = 'iptables'
IPTABLES_RULE = '-I INPUT -s {} -p udp --dport 123 -j NFQUEUE'.format(GUEST_IP)
IPT_INPUT_CMD = '{} {}'.format(IPT, IPTABLES_RULE)
IPT_DELETE_CMD = '{} -D INPUT 1'.format(IPT)


def handlePacket(pkt):
    data = pkt.get_payload()
    sPkt = IP(data)
    rPkt = IP(src=sPkt[IP].dst, dst=sPkt[IP].src)/UDP(dport=123, sport=123)/NTP()

    print(sPkt.summary())

    pkt.drop()
    send(rPkt)


def main():
    nfqueue = NetfilterQueue()

    try:
        nfqueue.bind(0, handlePacket)
    except Exception as e:
        print('NTP: Exception: ' + str(e))
        raise e

    try:
        nfqueue.run()
    except KeyboardInterrupt as e:
        print('NTP: Stop server')
        raise e
    except Exception as e:
        print('NTP: Exception: ' + str(e))
        raise e
    finally:
        nfqueue.unbind()


if __name__ == '__main__':

    try:
        check_call(IPT_INPUT_CMD, shell=True)
    except CalledProcessError as e:
        print('NTP: Exception ' + str(e))
        exit(1)
    
    try:
        main()
    except KeyboardInterrupt as e:
        exit(0)
    except Exception as e:
        exit(1)
    finally:
        try:
            check_call(IPT_DELETE_CMD, shell=True)
        except CalledProcessError as e:
            print('NTP: Exception: ' + str(e))
            exit(1)
        else:
            exit(0)
