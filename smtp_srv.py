# NOTE: Must be run as root.
# NOTE: We use python socket's lib here because fiddling with TCP SEQ and
#       ACK numbers would be required when we use scapy & nfqueue to intercept
#       the traffic.
from select import select
from socket import AF_INET, IPPROTO_TCP, SOCK_STREAM, socket, SOL_SOCKET, \
    SO_REUSEADDR, SHUT_RDWR
from sys import exit
from traceback import print_exc
from time import sleep
from util import getAddresses


HOST_IP, _ = getAddresses('host')
PORTS = [25, 465, 587]


def createSocket(port):
    s = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP)
    s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    s.bind((HOST_IP, port))
    s.listen(1)
    print('SMTP: Start listening on {} port {}'.format(HOST_IP, port))

    return s


# Don't know how else to distinguish between a pure server socket and a
# client connection. Even though they are different objs a "s in srvSockets"
# still turns out to be true even though its the client object is a different
# one than the server socket that accepted the connection.
def isSrvSocket(s):
    try:
        s.getpeername()
    except:
        return True
    else:
        return False


def handlePacket(pkt):
    pass


def main(socketList):
    while True:
        rlist, _, _ = select(socketList, [], [])
        for s in rlist:
            if isSrvSocket(s):
                c, addr = s.accept()
                print('SMTP: Client connected from ' + str(addr))
                socketList.append(c)
            else:
                addr = s.getpeername()[0]
                try:
                    data = s.recv(1024)
                except Exception as e:
                    print('SMTP: Exception: ' + str(e))
                    continue
                else:
                    if len(data) == 0:
                        print('SMTP: Client {} disconnected'.format(addr))
                        s.close()
                        socketList.remove(s)
                        continue
                    else:
                        print('SMTP: Received from {}: {}'.format(addr, data))

                reply = 'DUDE'
                try:
                    sent = s.send(reply)
                except Exception as e:
                    print('SMTP: Exception: ' + str(e))
                    continue
                else:
                    if sent == len(reply):
                        print('SMTP: Sent {} to {}'.format(reply, addr))
                    else:
                        print('SMTP: Failed to sent reply to ' + str(addr))


if __name__ == '__main__':
    socketList = []
    for p in PORTS:
        try:
            socketList.append(createSocket(p))
        except Exception as e:
            print('SMTP: Exception' + str(e))
            raise e

    try:
        main(socketList)
    except KeyboardInterrupt:
        print('SMTP: Stop server')
        exit(0)
    except Exception as e:
        print('SMTP: Exception: ' + str(e))
        print_exc()
        exit(1)
    finally:
        for s in socketList:
            s.shutdown(SHUT_RDWR)
            s.close()
