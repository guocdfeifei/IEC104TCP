# coding:utf-8
#author=guoff
#date  17:08
str1='09:0300:12' #类型:原因类型:分组长度
baowen = '68 10 00 00 00 00 09 02 03 00 01 00 01 40 00 01 00 00 02 40 00 02 00 00 '.replace(' ','')
'''
2021/3/3/ 17:21:23.295 TCP:14.115.31.1:2404 --> 14.10.10.2:42454 nbyte:<28>
68 1A 18 4E 1A 00 0D 02 03 00 03 00 63 09 00 8C 68 DB 3E 00 64 09 00 D7 9C 1B 3F 00 

68 1A 18 4E 1A 00 0D
00 63 09 00 8C 68 DB 3E 
00 64 09 00 D7 9C 1B 3F 00 



I格式报文 发送序列号: 9996 接收序列号: 13 
测量值,短浮点数(13) 单个信息寻址,信息总数:2 突发(3) ASDU地址:3 
信息体地址:2403 值:0.428532 
信息体地址:2404 值:0.607862 
'''
str1list = str1.split(':')
ti = baowen[12:14] #类型
vsq = int(baowen[14:16], 16) #长度
resan = baowen[16:20] #原因
if ti==str1list[0] and vsq>0 and resan ==str1list[1]:
    datalist=[]
    beginindex = 20+4 #原因后面有公共地址，开始
    while True:
        tmpstr = baowen[beginindex:beginindex+int(str1list[2])]
        print('开始循环获取',tmpstr)

        if len(tmpstr)>0:
            addtmp1 = tmpstr[:6]
            valuetmp = tmpstr[6:10]
            tmpadd = {'add':addtmp1[2:4]+addtmp1[:2],'value':valuetmp[2:4]+valuetmp[:2]}
            datalist.append(tmpadd)
            beginindex = beginindex+int(str1list[2])
        else:
            break
    print('datalist',datalist)


# print('addinf',addinf)