# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'basicParameterSettingsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_basicParameterSettingsWindow(object):
    def setupUi(self, basicParameterSettingsWindow):
        basicParameterSettingsWindow.setObjectName("basicParameterSettingsWindow")
        basicParameterSettingsWindow.resize(921, 710)
        self.centralwidget = QtWidgets.QWidget(basicParameterSettingsWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(10, 30, 821, 261))
        self.label2.setStyleSheet("font: 28pt \"微软雅黑\";\n"
"font: 18pt \"Adobe Devanagari\";\n"
"font: 14pt \"Adobe Devanagari\";")
        self.label2.setObjectName("label2")
        self.label1 = QtWidgets.QLabel(self.centralwidget)
        self.label1.setGeometry(QtCore.QRect(10, 280, 111, 16))
        self.label1.setObjectName("label1")
        self.lineEditBasicParameterAddress = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditBasicParameterAddress.setGeometry(QtCore.QRect(120, 280, 631, 21))
        self.lineEditBasicParameterAddress.setObjectName("lineEditBasicParameterAddress")
        self.pushButtonBasicParameterChoice = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonBasicParameterChoice.setGeometry(QtCore.QRect(770, 280, 51, 20))
        self.pushButtonBasicParameterChoice.setStyleSheet("background-color: rgb(177, 177, 177);")
        self.pushButtonBasicParameterChoice.setObjectName("pushButtonBasicParameterChoice")
        self.labelBasicParameterImage = QtWidgets.QLabel(self.centralwidget)
        self.labelBasicParameterImage.setGeometry(QtCore.QRect(470, 360, 240, 320))
        self.labelBasicParameterImage.setStyleSheet("# labelBasicParameterImage{\n"
"rgb(255, 255, 127)}")
        self.labelBasicParameterImage.setText("")
        self.labelBasicParameterImage.setObjectName("labelBasicParameterImage")
        self.pushButtonStartAdjust = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStartAdjust.setGeometry(QtCore.QRect(760, 350, 93, 28))
        self.pushButtonStartAdjust.setObjectName("pushButtonStartAdjust")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(360, 340, 72, 15))
        self.label.setObjectName("label")
        self.labelOriginalBasicParameterImage = QtWidgets.QLabel(self.centralwidget)
        self.labelOriginalBasicParameterImage.setGeometry(QtCore.QRect(80, 360, 240, 320))
        self.labelOriginalBasicParameterImage.setStyleSheet("# labelBasicParameterImage{\n"
"rgb(255, 255, 127)}")
        self.labelOriginalBasicParameterImage.setText("")
        self.labelOriginalBasicParameterImage.setObjectName("labelOriginalBasicParameterImage")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 340, 72, 15))
        self.label_2.setObjectName("label_2")
        basicParameterSettingsWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(basicParameterSettingsWindow)
        QtCore.QMetaObject.connectSlotsByName(basicParameterSettingsWindow)

    def retranslateUi(self, basicParameterSettingsWindow):
        _translate = QtCore.QCoreApplication.translate
        basicParameterSettingsWindow.setWindowTitle(_translate("basicParameterSettingsWindow", "基本参数设置"))
        self.label2.setText(_translate("basicParameterSettingsWindow", "1、由于照片的差异，需要手动调整一些参数，帮助系统更好的运行。\n"
"2、强度梯度小于minThresh的必定不是边缘\n"
"3、强度梯度大于maxThresh的必定是边缘\n"
"4、dilate会连接不连续部分\n"
"5、erode会丢弃边缘部分的像素，可能会造成不连续\n"
"6、请随机选择一批图片中的一张\n"
"7、点击Esc退出settings界面\n"
""))
        self.label1.setText(_translate("basicParameterSettingsWindow", "选择样例图片："))
        self.pushButtonBasicParameterChoice.setText(_translate("basicParameterSettingsWindow", "..."))
        self.pushButtonStartAdjust.setText(_translate("basicParameterSettingsWindow", "开始调整"))
        self.label.setText(_translate("basicParameterSettingsWindow", "处理结果："))
        self.label_2.setText(_translate("basicParameterSettingsWindow", "原图："))
