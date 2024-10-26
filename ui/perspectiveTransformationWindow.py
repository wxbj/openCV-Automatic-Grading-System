from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_perspectiveTransformationWindow(object):
    def setupUi(self, perspectiveTransformationWindow):
        perspectiveTransformationWindow.setObjectName("perspectiveTransformationWindow")
        perspectiveTransformationWindow.resize(802, 710)
        self.centralwidget = QtWidgets.QWidget(perspectiveTransformationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label2 = QtWidgets.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(10, 30, 701, 261))
        self.label2.setStyleSheet("font: 28pt \"微软雅黑\";\n"
"font: 18pt \"Adobe Devanagari\";\n"
"font: 14pt \"Adobe Devanagari\";")
        self.label2.setObjectName("label2")
        self.lineEditPerspectiveTransformationAddress = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditPerspectiveTransformationAddress.setGeometry(QtCore.QRect(30, 290, 631, 21))
        self.lineEditPerspectiveTransformationAddress.setObjectName("lineEditPerspectiveTransformationAddress")
        self.pushButtonpersPectiveTransformationChoice = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonpersPectiveTransformationChoice.setGeometry(QtCore.QRect(690, 290, 71, 20))
        self.pushButtonpersPectiveTransformationChoice.setStyleSheet("background-color: rgb(177, 177, 177);")
        self.pushButtonpersPectiveTransformationChoice.setObjectName("pushButtonpersPectiveTransformationChoice")
        self.labelPerspectiveTransformationImage = QtWidgets.QLabel(self.centralwidget)
        self.labelPerspectiveTransformationImage.setGeometry(QtCore.QRect(420, 360, 240, 320))
        self.labelPerspectiveTransformationImage.setStyleSheet("# labelBasicParameterImage{\n"
"rgb(255, 255, 127)}")
        self.labelPerspectiveTransformationImage.setText("")
        self.labelPerspectiveTransformationImage.setObjectName("labelPerspectiveTransformationImage")
        self.pushButtonStartAdjust = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStartAdjust.setGeometry(QtCore.QRect(680, 330, 93, 28))
        self.pushButtonStartAdjust.setObjectName("pushButtonStartAdjust")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(320, 340, 72, 15))
        self.label.setObjectName("label")
        self.labelOriginalperspectiveTransformationImage = QtWidgets.QLabel(self.centralwidget)
        self.labelOriginalperspectiveTransformationImage.setGeometry(QtCore.QRect(60, 360, 240, 320))
        self.labelOriginalperspectiveTransformationImage.setStyleSheet("# labelBasicParameterImage{\n"
"rgb(255, 255, 127)}")
        self.labelOriginalperspectiveTransformationImage.setText("")
        self.labelOriginalperspectiveTransformationImage.setObjectName("labelOriginalperspectiveTransformationImage")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 340, 72, 15))
        self.label_2.setObjectName("label_2")
        perspectiveTransformationWindow.setCentralWidget(self.centralwidget)
        self.statusBarPerspectiveTransformation = QtWidgets.QStatusBar(perspectiveTransformationWindow)
        self.statusBarPerspectiveTransformation.setObjectName("statusBarPerspectiveTransformation")
        perspectiveTransformationWindow.setStatusBar(self.statusBarPerspectiveTransformation)

        self.retranslateUi(perspectiveTransformationWindow)
        QtCore.QMetaObject.connectSlotsByName(perspectiveTransformationWindow)

    def retranslateUi(self, perspectiveTransformationWindow):
        _translate = QtCore.QCoreApplication.translate
        perspectiveTransformationWindow.setWindowTitle(_translate("perspectiveTransformationWindow", "透视变换"))
        self.label2.setText(_translate("perspectiveTransformationWindow", "1、由于照片的差异，需要手动调整一些参数，帮助系统更好的运行。\n"
"2、强度梯度小于minThresh的必定不是边缘\n"
"3、强度梯度大于maxThresh的必定是边缘\n"
"4、dilate会连接不连续部分\n"
"5、erode会丢弃边缘部分的像素，可能会造成不连续\n"
"6、请随机选择一批图片中的一张\n"
"7、点击Esc退出settings界面\n"
""))
        self.pushButtonpersPectiveTransformationChoice.setText(_translate("perspectiveTransformationWindow", "选择图片"))
        self.pushButtonStartAdjust.setText(_translate("perspectiveTransformationWindow", "开始调整"))
        self.label.setText(_translate("perspectiveTransformationWindow", "处理结果："))
        self.label_2.setText(_translate("perspectiveTransformationWindow", "原图："))
