# coding:utf-8
#author=guoff
#date  11:39
import struct
s = 'a69b64bf'
s = '14ae1f41'
import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s', filename='flo.log',
                    filemode='wb')
print(struct.unpack('f', s.decode('hex'))[0])
pasedata = '6812140000000d010300010001400012010000006812160000000d010300010001400012010000006812180000000d01030001000140001201000000'
pasedata = '6862080002000d91140001000140000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006a031341006b8d07410041140b410000000000000000000000'
while len(pasedata) > 0:
    tmppasedata = ''
    if '68' == pasedata[:2]:
        # 获取本地报文长度
        datalen = int(pasedata[2:4],16)
        tmppasedata = pasedata[:4+datalen*2]
        print('tmppasedata',tmppasedata)
        pasedata = pasedata[4+datalen*2:]
        if len(pasedata)==0:
            break

slavData  = '6862080002000d91140001000140000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000006a031341006b8d07410041140b410000000000000000000000'
marchlist = '0d;0300;16'.split(';')
#解析总召数据
logging.info('0解析配置数据{0}'.format(slavData))
ti = slavData[12:14]  # 类型
vsq = int(slavData[14:16], 16)  # 长度 int(aa[14:16], 16)
resan = slavData[16:20]  # 原因
logging.debug('1解析配置数据{0}{1}'.format(ti,marchlist[0]))
#判断是否总召唤数据，若是则完成解析和数据匹配
datalist=[]
if ti == marchlist[0] and vsq > 0 and resan == '1400':
    logging.debug('2解析总召数据{0}'.format(slavData))
    beginindex = 24
    tmpstr = slavData[beginindex:beginindex+int(marchlist[2])] #first
    addtmp1 = tmpstr[:6]
    valuetmp = tmpstr[6:14]
    tmpadd = {'add': addtmp1[2:4] + addtmp1[:2],
              'value': struct.unpack('f', valuetmp.decode('hex'))[0]}  # valuetmp[2:4] + valuetmp[:2]}
    datalist.append(tmpadd)
    beginindex = beginindex + int(marchlist[2])
    logging.debug('2beginindex{} {}'.format(beginindex,datalist))
    datalen = int(marchlist[2])-6 #总召返回从第二位不带地址自加1完成地址
    tmpstr = slavData[beginindex:beginindex+datalen]
    beginindex = beginindex+datalen
    dataindex = 0
    while len(tmpstr)>=10:
        dataindex = dataindex +1
        tmpadd = {'add': hex(int(addtmp1[2:4] + addtmp1[:2],16)+dataindex)[2:],
                  'value': struct.unpack('f', tmpstr[:8].decode('hex'))[0]}  # valuetmp[2:4] + valuetmp[:2]}
        datalist.append(tmpadd)
        logging.debug('2beginindex{} {}'.format(beginindex, datalist))
        tmpstr = slavData[beginindex:beginindex + datalen]
        beginindex = beginindex + datalen

    logging.debug('3beginindex{} {}'.format(beginindex, datalist))

