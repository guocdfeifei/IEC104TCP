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
class conRelay():
    def __init__(self):


        self.relay = relayop()
        time.sleep(1)
        self.relay.closeall()
        time.sleep(1)
        self.state = 0

    def opRelay(self,Relay):
        if self.state == 0:
            self.relay.open(Relay)
            self.state = 1
        else:
            self.relay.close(Relay)
            self.state = 0

    # 继电器部分
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

# gshowStr = ''
def iec104(dst,cf,prcesstext,monitortext):
    conrelay = conRelay()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVTIMEO, struct.pack('ii', int(2), 0))  # 2 sec timeout
    try:
        sock.connect(dst)
    except:
        prcesstext.set('连接失败')
        return '连接失败', -1
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
    # C_IC_NA_1_broadcast = [
    #
    #     # iec 104 apci layer
    #     0x68,  # start
    #     0x0e,  # apdu len
    #     0x00, 0x00,  # type + tx
    #     0x00, 0x00,  # rx
    #
    #     # iec 104 asdu layer
    #     0x64,  # type id: C_IC_NA_1, interrogation command
    #     0x01,  # numix
    #     0x06,  # some stuff
    #     0x00,  # OA
    #     0x01, 0x00,  # addr 65535
    #     0x00,  # IOA
    #     0x00, 0x00, 0x14  # 0x14
    #
    # ]
    #
    # sock.send(''.join(map(chr, C_IC_NA_1_broadcast)))
    # recv = recv_from_socket(sock)
    # while not recv:
    #     recv = recv_from_socket(sock)
    #     time.sleep(0.5)
    # if recv:
    #     logging.info('{0}'.format(dst))
    #     logging.debug('iec104 C_IC_NA_1_broadcast : recv: %s' % recv.encode('hex'))
    #     # print "recv: %r" % recv
    #     print "c_ic_na_1 recv: %s" % recv.encode('hex')
    # else:
    #     print 'c_ic_na_1_broadcast: nothing received'
    #     return recv, -1
    # 收到测试帧，反馈 680443000000
    logging.info('解析配置数据{0}'.format(cf.get("app", "checkdata")))
    checklist = cf.get("app", "checkdata").split(';')
    marchlist = cf.get("app", "march").split(';')
    checkedlist = [1] * len(checklist)  # 校验后的值列表
    showStrlist = {}
    for tmp1 in checklist:
        tmp1list = tmp1.split(',')
        showStrlist[tmp1list[1]]=tmp1list[3]

    #等待总召唤数据传入
    print('等待总召唤数据传入')
    while True:
        recv = recv_from_socket(sock)
        while not recv:
            recv = recv_from_socket(sock)
            time.sleep(0.5)
            #超过1秒中没响应，则触发s帧
        if recv:
            logging.info('{0}'.format(dst))
            logging.debug('iec104 C_IC_NA_1_broadcast : recv: %s' % recv.encode('hex'))
            # print "recv: %r" % recv
            print "c_ic_na_1 recv: %s" % recv.encode('hex')

            def doCheckData(slavData):
                # gshowStr=''
                showStr = ''
                logging.info('解析配置数据{0}'.format(slavData))
                ti = slavData[12:14]  # 类型
                vsq = int(slavData[14:16], 16)  # 长度
                resan = slavData[16:20]  # 原因
                # logging.debug('解析配置数据: ti=%s  resan = %s ' % ti,resan)
                if ti == marchlist[0] and vsq > 0 and resan == marchlist[1]:
                    datalist = []
                    beginindex = 20 + 4  # 原因后面有公共地址，开始
                    while True:
                        tmpstr = slavData[beginindex:beginindex + int(marchlist[2])]
                        # print('开始循环获取', tmpstr)
                        logging.debug('开始循环获取: %s' % tmpstr)
                        if len(tmpstr) > 0:
                            addtmp1 = tmpstr[:6]
                            valuetmp = tmpstr[6:10]
                            tmpadd = {'add': addtmp1[2:4] + addtmp1[:2], 'value': valuetmp[2:4] + valuetmp[:2]}
                            datalist.append(tmpadd)
                            beginindex = beginindex + int(marchlist[2])
                        else:
                            break
                    # print('datalist', datalist)
                    logging.debug('获取数据列表datalist: %s' % datalist)

                    i = 0
                    for subcheck in checklist:
                        subChecklist= subcheck.split(',')
                        for tmpdata in datalist:
                            if subChecklist[0]==tmpdata['add']:
                                print('待分析数据',slavData) #00341200
                                # hexdata = slavData[len(subChecklist[0])+4:2]+slavData[len(subChecklist[0])+2:2]
                                # if gshowStr == '':
                                #     gshowStr = subChecklist[1] + ":" + str(
                                #         int(tmpdata['value'], 16) * float(subChecklist[2])) + "  "
                                # else:
                                #     gshowStr = gshowStr + subChecklist[1]+":"+str(int(tmpdata['value'], 16)*float(subChecklist[2]))+"  "

                                showStrlist[subChecklist[1]] = str(int(tmpdata['value'], 16)*float(subChecklist[2]))
                                logging.debug('showStrlist[subChecklist[1]] : %s' % showStrlist[subChecklist[1]] )
                                if showStrlist[subChecklist[1]]<subChecklist[3] :
                                    # checkedStr = checkedStr+'0'
                                    checkedlist[i]=0
                                else:
                                    checkedlist[i]=1
                            # else:
                            #     # showStr = showStr + subChecklist[1] + ":" + subChecklist[3]  + "  "
                            #     checkedlist[i] = 1
                            i = i+1

                    checkedStr = ''
                    for tmpchecked in checkedlist:
                        checkedStr = checkedStr+str(tmpchecked)
                    # gshowStr = gshowStr + showStr
                    showstr = ''
                    for tmpobj in showStrlist.keys():
                        showstr = showstr + tmpobj + ":" +showStrlist[tmpobj] +'\n'
                    monitortext.set(showstr)
                    logging.info('解析突发数据{0}'.format(checkedStr))
                    # num = (len(checkedStr) - len(checkedStr.replace('0', "")))
                    if len(checkedStr.replace('0', ""))==0:
                        logging.info('满足触发开关条件{0}'.format(checkedStr))
                        if conrelay.state == 0:
                            conrelay.opRelay(1)
                    else:
                        logging.info('不满足触发开关条件{0}'.format(checkedStr))
                        if conrelay.state == 1:
                            conrelay.opRelay(1)
                else:
                    logging.info('不满解析条件{0}'.format(marchlist))
            if recv.encode('hex')=='680443000000':
                prcesstext.set('监控中')
                TESTFR = [
                    # iec 104 apci layer
                    0x68,  # start
                    0x04,  # APDU len
                    0x83,  # type 0100 0011
                    0x00, 0x00, 0x00  # padding

                ]

                sock.send(''.join(map(chr, TESTFR)))
                time.sleep(0.5)
            elif len(recv.encode('hex'))>0 and recv.encode('hex')[12:14]=='09': #判断类型为遥测数据
                logging.info('解析配置数据{0}'.format(cf.get("app", "checkdata")))
                doCheckData(recv.encode('hex'))
            else:
                logging.info('未解析的返回数据{0}'.format(recv.encode('hex')))


    #监控遥测信息变化，变化后会主动发送么？还是需要被动查看？

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
    '''
    配置文件：
    从站ip，端口
    监听间隔秒
    要显示的值位置，名称，系数，阈值
    继电器满足条件：全部低于阈值
    
    '''

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