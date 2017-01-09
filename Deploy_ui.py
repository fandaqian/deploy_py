# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Deploy_ui.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(581, 298)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(60, 140, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(60, 190, 491, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(210, 150, 241, 21))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(60, 50, 54, 12))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(60, 90, 61, 16))
        self.label_3.setObjectName("label_3")
        self.warLocation = QtWidgets.QLineEdit(self.centralwidget)
        self.warLocation.setGeometry(QtCore.QRect(210, 40, 311, 31))
        self.warLocation.setObjectName("warLocation")
        self.tomcatLocation = QtWidgets.QLineEdit(self.centralwidget)
        self.tomcatLocation.setGeometry(QtCore.QRect(210, 90, 311, 31))
        self.tomcatLocation.setObjectName("tomcatLocation")
        self.msg = QtWidgets.QLabel(self.centralwidget)
        self.msg.setGeometry(QtCore.QRect(60, 230, 461, 21))
        self.msg.setText("")
        self.msg.setObjectName("msg")

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Deploy author:Fandaqian"))
        self.pushButton.setText(_translate("MainWindow", "发布"))
        self.label.setText(_translate("MainWindow", "请先将WAR包上传至文件夹再运行本程序"))
        self.label_2.setText(_translate("MainWindow", "WAR包路径"))
        self.label_3.setText(_translate("MainWindow", "Tomcat路径"))
        self.warLocation.setText(_translate("MainWindow", "D:\\ftpRoot"))
        self.tomcatLocation.setText(_translate("MainWindow", "D:\\tomcat"))
