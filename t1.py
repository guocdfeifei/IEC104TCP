# coding:utf-8
from ctypes import *

import time

class relayop():
    def __init__(self):
        self.dll = CDLL("usb_relay_device.dll")
        # lib = cdll.LoadLibrary("./usb_relay_device.lib")
        print(self.dll.usb_relay_init())
        aa = self.dll.usb_relay_device_enumerate()
        print('设备清单',aa)
        self.bb = self.dll.usb_relay_device_open(aa)
        print('打开设备',self.bb)
# status = c_int(0)
# print('打开设备',dll.usb_relay_device_get_status(aa,byref(status)))
# print('status',status.value)
    def openall(self):
        print('打开所有',self.dll.usb_relay_device_open_all_relay_channel(self.bb))
    def open(self,num):
        flag = self.dll.usb_relay_device_open_one_relay_channel(self.bb, num)
        print('打开', flag)
        return flag
    def close(self,num):
        flag = self.dll.usb_relay_device_close_one_relay_channel(self.bb, num)
        print('关闭', flag)
        return flag
# print('打开',dll.usb_relay_device_open_one_relay_channel(bb,1))
# for i in range(1,5):
#     # print('暂停1s')
#     time.sleep(1)
#     print('打开',i,dll.usb_relay_device_open_one_relay_channel(bb,i))
#
# for i in range(1,5):
#     # print('暂停1s')
#     time.sleep(1)
#     print('关闭',i,dll.usb_relay_device_close_one_relay_channel(bb,i))
    def closeall(self):
        # time.sleep(10)
        print('关闭所有',self.dll.usb_relay_device_close_all_relay_channel(self.bb))


#继电器部分
relay = relayop()
time.sleep(1)
relay.closeall()
time.sleep(1)
state = 0


def opRelay(Relay):
    global state
    if state == 0:
        relay.open(Relay)
        state = 1
    else:
        relay.close(Relay)
        state = 0


for i in range(10):
    opRelay(1)
    time.sleep(1)