# coding:utf-8
#author=guoff
#date  11:39
import struct
s = 'a69b64bf'
s = '14ae1f41'

print(struct.unpack('f', s.decode('hex'))[0])
