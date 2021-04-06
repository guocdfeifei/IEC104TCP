#-*- coding:utf-8 -*-
#author=guoff
#date  14:22
#!/usr/bin/env python
import threading
import datetime
import time
import os, sys
import ConfigParser
from t1 import relayop

from iec104 import iec104

if sys.version_info[0] == 2:
    from Tkinter import *
    from ttk import *
    #Usage:showinfo/warning/error,askquestion/okcancel/yesno/retrycancel
    from tkMessageBox import *
    #Usage:f=tkFileDialog.askopenfilename(initialdir='E:/Python')
    #import tkFileDialog
    #import tkSimpleDialog
else:  #Python 3.x
    from tkinter import *
    from tkinter.ttk import *
    from tkinter.messagebox import *
    from tkinter import StringVar, IntVar, scrolledtext
    #import tkinter.filedialog as tkFileDialog
    #import tkinter.simpledialog as tkSimpleDialog    #askstring()

def thread_it(func, *args):
    '''将函数打包进线程'''
    # 创建
    t = threading.Thread(target=func, args=args)
    # 守护 !!!
    t.setDaemon(True)
    # 启动
    t.start()
    # 阻塞--卡死界面！
    # t.join()


class conRelay():
    def __init__(self):

        # logging.info('{0}'.format(dst))
        self.relay = relayop()
        time.sleep(1)
        self.relay.closeall()
        time.sleep(1)
        self.state = 0
        # self.opRelay(1)

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


class Application_ui(Frame):
    #这个类仅实现界面生成功能，具体事件处理代码在子类Application中。
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('琪睿监控助手--正式版--山西琪睿科技')
        self.master.geometry('439x339')
        self.defaultModel = 1
        self.createWidgets()
        self.prcesstext.set('正在读取配置文件')
        self.cf = ConfigParser.ConfigParser()
        self.conrelay = conRelay()

        self.cf.read("iec104.conf")

        # read by type
        self.slave_host = self.cf.get("slave", "host")
        self.slave_port = self.cf.getint("slave", "port")
        self.defaultModel = self.cf.getint("app", "defaultmodel")
        print('self.defaultModel',self.defaultModel)
        self.v.set(self.defaultModel)
        self.showv()


    def printinfo(self,info,a):
        b = datetime.datetime.now()
        k=b-a
        self.text1.insert(INSERT, info+'\t耗时：'+str(k.total_seconds()) + '\n')
        self.text1.see(END)

    def closeyou(self):
        print('关闭油机')
        if self.conrelay.state == 1:
            self.conrelay.opRelay(1)
            showinfo('提示', '油机关闭成功', parent=self.master)
        else:
            # tkinter.messagebox.showinfo('提示', '油机已关闭')
            showinfo('提示', '油机已关闭', parent=self.master)
            # self.conrelay.opRelay(1)
    def showv(self):
        print('showv',self.v.get())
        if self.v.get()==1:
            self.hi_there3['state']=DISABLED
        else:
            self.hi_there3['state']=''
    def gethtmldata(self,page=1):
        '''
        :param page:
        :return:
        1、读取配置文件
        2、初始化变量
        '''


        # a = datetime.datetime.now()
        # self.printinfo('待处理:'+str(db_host),a)
        self.prcesstext.set('正在读取配置文件'+self.slave_host)
        import datetime
        end_date = datetime.datetime.strptime("2099-08-20", "%Y-%m-%d")
        datetimenowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # 现在
        begin_date = datetime.datetime.strptime(datetimenowTime, "%Y-%m-%d %H:%M:%S")
        if begin_date <= end_date:
            print('还可以用')
            dst = (self.slave_host, self.slave_port)
            recv, asdu_addr = iec104(dst,self.cf,self.prcesstext,self.monitortext,self.conrelay,self.v)
            print(recv, asdu_addr)
            # fileslist=list(set(self.needlist).difference(set(self.hadlist)).difference(set(self.errlist)))
            # #处理当前目录和失败目录共有的文件
            # doublelist = list(set(self.needlist).intersection(set(self.errlist)))
            # for delfile in doublelist:
            #     os.remove(os.path.join(self.filepath,delfile))
            # for file in fileslist:
            #     print('开始处理文件:',file)
            #     try:
            #         fileinfo = {
            #             'path':self.filepath,
            #             'succ':self.succpath,
            #             'err':self.errpath,
            #             'file':file
            #         }
            #         print("self.fileinfo['path'], self.fileinfo['file'])",fileinfo['path'], fileinfo['file'])
            #         a = datetime.datetime.now()
            #         aa = getinfo(fileinfo, self.e1.get())
            #
            #         # aa.getdocxinfo(r'D:\do\201907\批量简历\简历\金-李超.docx')
            #         # aa.getdocxinfo(r'D:\do\201907\批量简历\简历\前圆通汇报CIO(1)(1).docx')
            #         # aa.getdocxinfo(r'D:\do\201907\批量简历\简历\王军.docx')
            #         aa.getdocxinfo(self.printinfo)
            #
            #     except Exception as e:
            #         print('oops!解析出错!')
            #         self.printinfo('异常:'+str(e), a)
            #         print(e)
            #         # shutil.move(os.path.join(fileinfo['path'], fileinfo['file']),os.path.join(fileinfo['err'], fileinfo['file']))
            #         # doc.save(os.path.join(self.fileinfo['err'], self.fileinfo['file']))
            #         # os.remove(os.path.join(self.fileinfo['path'], self.fileinfo['file']))
            #         # aa.doexcept()
            #     finally:
            #         print("执行完成文件：",file)
            #
            #     self.printinfo('处理文件'+file, a)
            #     # fileslist.remove(file)
            #     time.sleep(1)

        else:
            showinfo('No', '试用期结束，请联系guoff.taobao.com')

    def createWidgets(self):
        self.top = self.winfo_toplevel()

        self.style = Style()

        self.TabStrip1 = Notebook(self.top)
        self.TabStrip1.place(relx=0.062, rely=0.071, relwidth=0.887, relheight=0.876)

        self.TabStrip1__Tab1 = Frame(self.TabStrip1)

        self.prcesstext = StringVar()
        self.prcesstext.set('准备执行')
        self.TabStrip1__Tab1Lbl = Label(self.TabStrip1__Tab1, textvariable=self.prcesstext)
        self.TabStrip1__Tab1Lbl.place(relx=0.1,rely=0.9)


        self.monitortext = StringVar()
        self.monitortext.set('监控数据：')
        self.TabStrip1__Tab1Lbl = Label(self.TabStrip1__Tab1, textvariable=self.monitortext)
        self.TabStrip1__Tab1Lbl.place(relx=0.1,rely=0.3)



        # self.CheckVar1 = IntVar()
        # self.C1 = Checkbutton(self.TabStrip1__Tab1, text="使用钱包余额抵扣", variable=self.CheckVar1, \
        #                  onvalue=1, offvalue=0)
        # self.C1.place(relx=0.1, rely=0)
        # self.label1 = Label(self.TabStrip1__Tab1, text="登陆cookie：")#.grid(row=0, column=0, padx=15, pady=5) , font=("华康少女字体", 15), fg="blue"
        # self.label1.place(relx=0.1, rely=0.1)
        # self.label2 = Label(self.TabStrip1__Tab1, text="注意事项：将执行文件放到简历文件夹内")#.grid(row=1, column=0, padx=15, pady=5) , font=("华康少女字体", 15), fg="red"
        # self.label2.place(relx=0.1, rely=0.2)
        # self.label2 = Label(self.TabStrip1__Tab1, text="支付cookie：")#.grid(row=1, column=0, padx=15, pady=5) , font=("华康少女字体", 15), fg="red"
        # self.label2.place(relx=0.1, rely=0.3)
        # self.label2 = Label(self.TabStrip1__Tab1, text="间隔时间s：")#.grid(row=1, column=0, padx=15, pady=5) , font=("华康少女字体", 15), fg="red"
        # self.label2.place(relx=0.1, rely=0.4)
        # label = Label(frame, text="抓取信息：", font=("华康少女字体", 15), fg="red").grid(row=7, column=0, padx=5, pady=1)

        # self.e1 = Entry(self.TabStrip1__Tab1, foreground='blue', font=('Helvetica', '12'))
        # # self.e2 = Entry(self.TabStrip1__Tab1, font=('Helvetica', '12', 'bold'))
        # # self.e3 = Entry(self.TabStrip1__Tab1, font=('Helvetica', '12', 'bold'))
        # # self.e3.insert(10, "")
        # # self.e4 = Entry(self.TabStrip1__Tab1, font=('Helvetica', '12', 'bold'))
        # # self.e4.insert(10, "2")
        # self.e1.insert(10, "")

        # self.e2.insert(10, "")
        # e1.grid(row=0, column=1)
        # e2.grid(row=1, column=1)
        # self.e1.place(relx=0.4, rely=0.1)
        # # self.e2.place(relx=0.4, rely=0.2)
        # # self.e3.place(relx=0.4, rely=0.3)
        # # self.e4.place(relx=0.4, rely=0.4)
        # self.hi_there1 = Button(self.TabStrip1__Tab1, text="简历目录", command=lambda :thread_it(self.selectpath)) #, font=("宋体", 15), width=6, command=self.gethtmldata
        # self.hi_there1.place(relx=0.1, rely=0.5)
        #.grid(row=2, column=0, padx=15, pady=5)

        self.hi_there2 = Button(self.TabStrip1__Tab1, text="开始监控", command=lambda :thread_it(self.gethtmldata, 1))#, font=("宋体", 15), width=6
        self.hi_there2.place(relx=0.3, rely=0.1)
        # #.grid(row=2, column=1, padx=15,pady=5)
        self.v = IntVar()


        self.radio1=Radiobutton(self.TabStrip1__Tab1, text='自动', variable=self.v, value=1, command = self.showv)#.pack(anchor=W)
        self.radio2 =Radiobutton(self.TabStrip1__Tab1, text='手动', variable=self.v, value=2,command = self.showv )#.pack(anchor=W)
        self.radio1.place(relx=0.01, rely=0.1)
        self.radio2.place(relx=0.15, rely=0.1)

        self.hi_there3 = Button(self.TabStrip1__Tab1, text="关闭油机", command=self.closeyou)#, font=("宋体", 15), width=6
        self.hi_there3.place(relx=0.6, rely=0.1)
        #.grid(row=2, column=2, padx=15,pady=5)
        # self.hi_there.pack()
        # self.text1 = scrolledtext.ScrolledText(self.TabStrip1__Tab1, width=125, height=6) #, font=("华康少女字体", 15)
        #
        # # text.grid(row=3, column=0, padx=35, pady=5, columnspan=2)
        # self.text1.place(relx=0.1, rely=0.6)
        self.TabStrip1.add(self.TabStrip1__Tab1, text='监控')


        # scroll = Scrollbar()
        # scroll.pack(side=RIGHT, fill=Y)
        # scroll.config(command=self.text1.yview)
        # self.text1.config(yscrollcommand=scroll.set)

        # self.text1['yscrollcommand'] = scroll.set
        # # for i in range(100):
        # #     lb.insert(END, str(i))
        # # self.text1.pack(side=LEFT)
        # scroll['command'] = self.text1.yview



class Application(Application_ui):
    #这个类实现具体的事件处理回调函数。界面生成代码在Application_ui中。
    def __init__(self, master=None):
        Application_ui.__init__(self, master)

if __name__ == "__main__":
    top = Tk()
    Application(top).mainloop()
