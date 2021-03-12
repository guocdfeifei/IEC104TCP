# coding:utf-8
#!/usr/bin/env python

"""
File: iec-60870-5-104.py
Desc: iec-60870-5-104 (IEC 104) protocol tool:

"""
import time

from t1 import relayop

__author__ = "Aleksandr Timorin"
__copyright__ = "Copyright 2013, Positive Technologies"
__license__ = "GNU GPL v3"
__version__ = "1.0"
__maintainer__ = "Aleksandr Timorin"
__email__ = "atimorin@gmail.com"
__status__ = "Development"

import os
import sys
import logging
import socket
import struct

from os.path import abspath
from os.path import join as jpath

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='iec-60870-5-104.log',
                    filemode='wb')


# dst = ('192.168.163.130', 2404)
# dst = ('127.0.0.1', 2404)
# dst = ('10.1.76.97', 2404)

def recv_from_socket(sock, rsize=1):
    recv = ''
    try:
        while True:
            r = sock.recv(rsize)
            if r:
                recv += r
            else:
                break
    except:
        pass
        # print str(sys.exc_info())
    return recv


def iec104(dst):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('ii', int(2), 0))  # 2 sec timeout
    try:
        sock.connect(dst)
    except:
        return '', -1
    # =========================================================================
    #创建链接  主站连接子站时，主站给子站发送一个U帧启动报文
    TESTFR = [
        # iec 104 apci layer
        0x68,  # start
        0x04,  # APDU len
        0x07,  # type 0100 0011
        0x00, 0x00, 0x00  # padding

    ]

    sock.send(''.join(map(chr, TESTFR)))
    recv = recv_from_socket(sock)
    # print "0testfr recv: %s" % recv
    while not recv:
        recv = recv_from_socket(sock)
        time.sleep(0.5)
        # logging.info('{0}'.format(dst))
        # print "testfr recv: %s" % recv
        # logging.debug('iec104 TESTFR : recv: %s' % recv.encode('hex'))
        # # print "testfr recv: %r" % recv
        # print "testfr recv: %s" % recv.encode('hex')

    if recv:
        logging.info('{0}'.format(dst))
        print "testfr recv: %s" % recv
        logging.debug('iec104 TESTFR : recv: %s' % recv.encode('hex'))
        # print "testfr recv: %r" % recv
        print "testfr recv: %s" % recv.encode('hex')
    else:
        print "testfr: nothing received"
        return recv, -1

    # 接收→确认激活传输启动
    TESTFR = [
        # iec 104 apci layer
        0x68,  # start
        0x04,  # APDU len
        0x0B,  # type 0100 0011
        0x00, 0x00, 0x00  # padding

    ]

    sock.send(''.join(map(chr, TESTFR)))
    recv = recv_from_socket(sock)
    # print "0testfr recv: %s" % recv
    while not recv:
        recv = recv_from_socket(sock)
        time.sleep(0.5)
    if recv:
        logging.info('{0}'.format(dst))
        logging.debug('iec104 STARTDT : recv: %s' % recv.encode('hex'))
        # print "recv: %r" % recv
        print "startdt recv: %s" % recv.encode('hex')
    else:
        print 'startdt: nothing received'
        return recv, -1

    # =========================================================================
    # #获取数据
    # STARTDT = [
    #     # iec 104 apci layer
    #     0x68,  # start
    #     0x04,  # APDU len
    #     0x43,  # type 0000 0111
    #     0x00, 0x00, 0x00  # padding
    # ]
    #
    # sock.send(''.join(map(chr, STARTDT)))
    # recv = recv_from_socket(sock)
    # while not recv:
    #     recv = recv_from_socket(sock)
    #     time.sleep(0.5)
    # if recv:
    #     logging.info('{0}'.format(dst))
    #     logging.debug('iec104 STARTDT : recv: %s' % recv.encode('hex'))
    #     # print "recv: %r" % recv
    #     print "startdt recv: %s" % recv.encode('hex')
    # else:
    #     print 'startdt: nothing received'
    #     return recv, -1
    #
    # # if received 2 packets - STARTDT con + ME_EI_NA_1 Init  - full length should be 6+6+10 bytes
    # if len(recv) == 22:
    #     asdu_addr, = struct.unpack('<H', recv[16:18])
    #     print "ASDU address: %d" % asdu_addr
    #     sock.close()
    #     return recv, asdu_addr
    # =========================================================================
    #发起总召唤
    C_IC_NA_1_broadcast = [

        # iec 104 apci layer
        0x68,  # start
        0x0e,  # apdu len
        0x00, 0x00,  # type + tx
        0x00, 0x00,  # rx

        # iec 104 asdu layer
        0x64,  # type id: C_IC_NA_1, interrogation command
        0x01,  # numix
        0x06,  # some stuff
        0x00,  # OA
        0x01, 0x00,  # addr 65535
        0x00,  # IOA
        0x00, 0x00, 0x14  # 0x14

    ]

    sock.send(''.join(map(chr, C_IC_NA_1_broadcast)))
    recv = recv_from_socket(sock)
    while not recv:
        recv = recv_from_socket(sock)
        time.sleep(0.5)
    if recv:
        logging.info('{0}'.format(dst))
        logging.debug('iec104 C_IC_NA_1_broadcast : recv: %s' % recv.encode('hex'))
        # print "recv: %r" % recv
        print "c_ic_na_1 recv: %s" % recv.encode('hex')
    else:
        print 'c_ic_na_1_broadcast: nothing received'
        return recv, -1

    # 接收→S帧
    print("接收→S帧")
    STARTDT = [
        # iec 104 apci layer
        0x68,  # start
        0x04,  # APDU len
        0x01,  # type 0000 0111
        0x00, 0x02, 0x00  # padding
    ]
    sock.send(''.join(map(chr, STARTDT)))
    recv = recv_from_socket(sock)
    while not recv:
        recv = recv_from_socket(sock)
        time.sleep(0.5)
    if recv:
        logging.info('{0}'.format(dst))
        logging.debug('iec104 C_IC_NA_1_broadcast : recv: %s' % recv.encode('hex'))
        # print "recv: %r" % recv
        print "c_ic_na_1 recv: %s" % recv.encode('hex')
    else:
        print 'c_ic_na_1_broadcast: nothing received'
        return recv, -1

    #接收→总召唤确认 680401000200
    if recv.encode('hex') == '680401000200':
        #发送确认命令
        print("发送确认命令")
        # 发起总召唤确认命令
        C_IC_NA_1_broadcast = [

            # iec 104 apci layer
            0x68,  # start
            0x0e,  # apdu len
            0x00, 0x00,  # type + tx
            0x00, 0x00,  # rx

            # iec 104 asdu layer
            0x64,  # type id: C_IC_NA_1, interrogation command
            0x01,  # numix
            0x06,  # some stuff
            0x00,  # OA
            0x01, 0x00,  # addr 65535
            0x00,  # IOA
            0x00, 0x00, 0x14  # 0x14

        ]

        sock.send(''.join(map(chr, C_IC_NA_1_broadcast)))
        recv = recv_from_socket(sock)
        while not recv:
            recv = recv_from_socket(sock)
            time.sleep(0.5)
        if recv:
            logging.info('{0}'.format(dst))
            logging.debug('iec104 STARTDT : recv: %s' % recv.encode('hex'))
            # print "recv: %r" % recv
            print "startdt recv: %s" % recv.encode('hex')
        else:
            print 'startdt: nothing received'
            return recv, -1

        #发送S帧
        print("发送S帧")
        STARTDT = [
            # iec 104 apci layer
            0x68,  # start
            0x04,  # APDU len
            0x01,  # type 0000 0111
            0x00, 0x02, 0x00  # padding
        ]
        sock.send(''.join(map(chr, STARTDT)))
        #接收→总召唤确认
        print("接收→总召唤确认")
        C_IC_NA_1_broadcast = [

            # iec 104 apci layer
            0x68,  # start
            0x0e,  # apdu len
            0x00, 0x00,  # type + tx
            0x00, 0x00,  # rx

            # iec 104 asdu layer
            0x64,  # type id: C_IC_NA_1, interrogation command
            0x01,  # numix
            0x07,  # some stuff
            0x00,  # OA
            0x01, 0x00,  # addr 65535
            0x00,  # IOA
            0x00, 0x00, 0x14  # 0x14

        ]

        sock.send(''.join(map(chr, C_IC_NA_1_broadcast)))


        #发送S帧
        print("发送S帧")
        STARTDT = [
            # iec 104 apci layer
            0x68,  # start
            0x04,  # APDU len
            0x01,  # type 0000 0111
            0x00, 0x02, 0x00  # padding
        ]
        sock.send(''.join(map(chr, STARTDT)))


        #接收→YX帧（以类型标识1为例）
        print("接收→YX帧（以类型标识1为例）")
        C_IC_NA_1_broadcast = [

            # iec 104 apci layer
            0x68,  # start
            0x1e,  # apdu len
            0x04, 0x00,  # type + tx
            0x02, 0x00,  # rx

            # iec 104 asdu layer
            0x03,  # type id: C_IC_NA_1, interrogation command
            0x05,  # numix
            0x14,  # some stuff
            0x01,  # OA
            0x00, 0x01,  # addr 65535
            0x00,  # IOA
            0x00, 0x02, 0x06, 0x00, 0x02 , 0x0A, 0x00, 0x00, 0x01 , 0x0B, 0x00, 0x00, 0x02 , 0x0C, 0x00, 0x00, 0x01 # 0x14

        ]

        sock.send(''.join(map(chr, C_IC_NA_1_broadcast)))


        #发送S帧
        print("发送S帧")
        STARTDT = [
            # iec 104 apci layer
            0x68,  # start
            0x04,  # APDU len
            0x01,  # type 0000 0111
            0x00, 0x02, 0x00  # padding
        ]
        sock.send(''.join(map(chr, STARTDT)))




        #接收→结束总召唤帧
        print("接收→结束总召唤帧")
        C_IC_NA_1_broadcast = [

            # iec 104 apci layer
            0x68,  # start
            0x0e,  # apdu len
            0x08, 0x00,  # type + tx
            0x02, 0x00,  # rx

            # iec 104 asdu layer
            0x64,  # type id: C_IC_NA_1, interrogation command
            0x01,  # numix
            0x0A,  # some stuff
            0x00,  # OA
            0x01, 0x00,  # addr 65535
            0x00,  # IOA
            0x00, 0x00, 0x14 # 0x14

        ]

        sock.send(''.join(map(chr, C_IC_NA_1_broadcast)))


        #发送S帧
        print("发送S帧")
        STARTDT = [
            # iec 104 apci layer
            0x68,  # start
            0x04,  # APDU len
            0x01,  # type 0000 0111
            0x00, 0x02, 0x00  # padding
        ]
        sock.send(''.join(map(chr, STARTDT)))


        recv = recv_from_socket(sock)
        while not recv:
            recv = recv_from_socket(sock)
            time.sleep(0.5)
        if recv:
            logging.info('{0}'.format(dst))
            logging.debug('iec104 C_IC_NA_1_broadcast : recv: %s' % recv.encode('hex'))
            # print "recv: %r" % recv
            print "c_ic_na_1 recv: %s" % recv.encode('hex')
        else:
            print 'c_ic_na_1_broadcast: nothing received'
            return recv, -1
    else:
        print(recv.encode('hex'))

    # print "recv: %s" % recv.encode('hex')
    try:
        assert len(recv) == 16
        asdu_addr, = struct.unpack('<H', recv[10:12])
        print "ASDU address: %d" % asdu_addr
    except:
        asdu_addr = -1
    finally:
        sock.close()

    return recv, asdu_addr


if __name__ == '__main__':

    # if len(sys.argv) == 2:
    #    dst = (sys.argv[1], 2404)
    # else:
    #    dst = ('127.0.0.1', 2404)

    for l in open(sys.argv[1]):
        ip = l.strip()
        if ip:
            print "process %s" % ip
            dst = (ip, 2404)
            recv, asdu_addr = iec104(dst)
            print "ip: {0}, recv: {1}, asdu_addr: {2}".format(ip, recv.encode('hex'), asdu_addr)

    #继电器部分
    # relay = relayop()
    # time.sleep(1)
    # relay.closeall()
    # time.sleep(1)
    # state = 0
    #
    #
    # def opRelay(Relay):
    #     global state
    #     if state == 0:
    #         relay.open(Relay)
    #         state = 1
    #     else:
    #         relay.close(Relay)
    #         state = 0
    #
    #
    # for i in range(10):
    #     opRelay(1)
    #     time.sleep(1)