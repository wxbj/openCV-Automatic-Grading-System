# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputAnswerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_inputAnswerWindow(object):
    def setupUi(self, inputAnswerWindow):
        inputAnswerWindow.setObjectName("inputAnswerWindow")
        inputAnswerWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(inputAnswerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelAnswerAddress = QtWidgets.QLabel(self.centralwidget)
        self.labelAnswerAddress.setGeometry(QtCore.QRect(30, 30, 111, 16))
        self.labelAnswerAddress.setObjectName("labelAnswerAddress")
        self.pushButtonChoice = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoice.setGeometry(QtCore.QRect(700, 30, 51, 20))
        self.pushButtonChoice.setStyleSheet("background-color: rgb(177, 177, 177);")
        self.pushButtonChoice.setObjectName("pushButtonChoice")
        self.lineEditAddress = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddress.setGeometry(QtCore.QRect(130, 30, 551, 21))
        self.lineEditAddress.setObjectName("lineEditAddress")
        self.textEditAnswer = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditAnswer.setGeometry(QtCore.QRect(30, 80, 721, 481))
        self.textEditAnswer.setObjectName("textEditAnswer")
        inputAnswerWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(inputAnswerWindow)
        QtCore.QMetaObject.connectSlotsByName(inputAnswerWindow)

    def retranslateUi(self, inputAnswerWindow):
        _translate = QtCore.QCoreApplication.translate
        inputAnswerWindow.setWindowTitle(_translate("inputAnswerWindow", "MainWindow"))
        self.labelAnswerAddress.setText(_translate("inputAnswerWindow", "选择答案地址："))
        self.pushButtonChoice.setText(_translate("inputAnswerWindow", "..."))
