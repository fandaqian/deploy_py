# -*- coding: utf-8 -*-
# pyinstaller -F -w  main.py

import os.path,time,shutil,zipfile,re

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from Deploy_ui import Ui_MainWindow

class delDictThread(QThread):
    # 声明一个信号，同时返回一个str
    trigger = pyqtSignal(int, str)
    #构造函数里增加形参
    def __init__(self, t, tomcat, parent=None):
        super(delDictThread, self).__init__(parent)
        #储存参数
        self.t = t
        self.tomcat = tomcat
        self.trigger.connect(self.sin2Call)

    def sin2Call(self, val, text):
        print("sin3 emit, value:", val, text)

    def countProcessMemoey(self):
        processName = 'java.exe';
        pattern = re.compile(r'([^\s]+)\s+(\d+)\s.*\s([^\s]+\sK)')
        cmd = 'tasklist /fi "imagename eq ' + processName + '"' + ' | findstr.exe ' + processName
        # tasklist /fi "imagename eq java.exe" | findstr.exe java.exe
        print(cmd)
        result = os.popen(cmd).read()
        resultList = result.split("\n")
        pid = 0
        max = 0

        for srcLine in resultList:
            srcLine = "".join(srcLine.split('\n'))
            if len(srcLine) == 0:
                break
            m = pattern.search(srcLine)
            if m == None:
                continue
            # 由于是查看python进程所占内存，因此通过pid将本程序过滤掉
            if str(os.getpid()) == m.group(2):
                continue
            ori_mem = m.group(3).replace(',', '')
            ori_mem = ori_mem.replace(' K', '')
            ori_mem = ori_mem.replace(r'\sK', '')
            memEach = int(ori_mem)
            if (max == 0 or max < memEach):
                max = memEach
                pid = int(m.group(2))
            print('ProcessName:' + m.group(1) + '\tPID:' + m.group(2) + '\tmemory size:%.2f' % (memEach * 1.0 / 1024), 'M')

        print('最大内存: ' + str(max) + ', PID: ' + str(pid))
        self.pid = pid

    #重写 run() 函数
    def run(self):
        dictWar = self.t
        now = time.time()
        print('当前时间戳：' + str(now))
        names = []

        for f1 in os.listdir(dictWar):
            full = os.path.join(dictWar, f1)
            if (os.path.isfile(full)):
                modifyTime = os.path.getmtime(full)
                strlist = f1.split('.')
                if (modifyTime >= now - 15 * 60 and strlist[-1] == 'war'):
                    print('文件: ' + f1 + ', 修改时间: ' + str(modifyTime))
                    names.append(f1)

        self.trigger.emit(10, "解析上传war包...")

        for f11 in names:
            strlist = f11.split('.')
            full = os.path.join(dictWar, strlist[-2])
            if (os.path.exists(full)):
                print('删除文件夹: ' + full)
                shutil.rmtree(full)
                print('建立文件夹: ' + full)
                os.mkdir(full)

        self.trigger.emit(20, "删除已解压文件...")

        i = 1
        for f11 in names:
            full = os.path.join(dictWar, f11)
            strlist = f11.split('.')
            dict = os.path.join(dictWar, strlist[-2])
            r = zipfile.is_zipfile(full)
            if r:
                fz = zipfile.ZipFile(full, 'r')
                for file in fz.namelist():
                    self.trigger.emit(20 + (5 * i), "解压文件..." + strlist[-2] + '/' + file)
                    fz.extract(file, dict)
            else:
                self.trigger.emit(20, 'This file is not zip file ' + full)
            i = i + 1

        self.countProcessMemoey()
        if (self.pid != 0):
            self.trigger.emit(50, "结束java进程...")
            command = 'taskkill /F /PID ' + str(self.pid)
            print(command)
            os.system(command)


        self.trigger.emit(55, "删除 Tomcat/logs 目录文件...")
        logsDict = os.path.join(self.tomcat, 'logs')
        shutil.rmtree(logsDict)
        os.mkdir(logsDict)
        self.trigger.emit(60, "删除 Tomcat/work 目录文件...")
        workDict = os.path.join(self.tomcat, 'work')
        shutil.rmtree(workDict)
        os.mkdir(workDict)

        self.trigger.emit(65, "删除 Tomcat/webapps 目录文件...")
        for f12 in names:
            strlist = f12.split('.')
            full = os.path.join(self.tomcat, 'webapps', strlist[-2])
            print('删除文件夹: ' + full)
            if (os.path.exists(full)):
                shutil.rmtree(full)

        self.trigger.emit(70, "复制解压文件至 Tomcat/webapps 目录...")
        b = 1
        for f13 in names:
            strlist = f13.split('.')
            dest = os.path.join(self.tomcat, 'webapps', strlist[-2])
            source = os.path.join(dictWar, strlist[-2])
            self.trigger.emit(70 + (b * 5), "复制文件..." + source + ' to ' + dest)
            shutil.copytree(source, dest)
            b = b + 1

        runBat = os.path.join(self.tomcat, 'bin', 'startup.bat');
        print('exec', runBat)
        os.system(runBat)
        self.trigger.emit(100, "启动Tomcat...")


class mywindow(QWidget, Ui_MainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.myClick)

    def myClick(self):
        self.msg.setText("开始运行...")
        self.progressBar.setProperty("value", 0)

        dictWar = self.warLocation.text()
        dictTomcat = self.tomcatLocation.text()

        # 创建线程
        thread = delDictThread(dictWar, dictTomcat)
        # 启动线程
        thread.start()
        # 注册信号处理函数
        thread.trigger.connect(self.delDictThreadEnd)


    def delDictThreadEnd(self, val, text):
        self.msg.setText(text)
        self.progressBar.setProperty("value", val)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    myshow = mywindow()
    myshow.show()
    sys.exit(app.exec_())
