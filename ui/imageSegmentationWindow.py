from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_imageSegmentationWindow(object):
    def setupUi(self, imageSegmentationWindow):
        imageSegmentationWindow.setObjectName("imageSegmentationWindow")
        imageSegmentationWindow.resize(809, 600)
        self.centralwidget = QtWidgets.QWidget(imageSegmentationWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 10, 751, 401))
        self.label.setStyleSheet("font: 12pt \"Adobe Devanagari\";\n"
"font: 14pt \"Adobe Devanagari\";")
        self.label.setObjectName("label")
        self.pushButtonImageSegmentation = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonImageSegmentation.setGeometry(QtCore.QRect(320, 500, 93, 28))
        self.pushButtonImageSegmentation.setObjectName("pushButtonImageSegmentation")
        self.lineEditAddressSegment = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddressSegment.setGeometry(QtCore.QRect(30, 440, 591, 21))
        self.lineEditAddressSegment.setText("")
        self.lineEditAddressSegment.setObjectName("lineEditAddressSegment")
        self.pushButtonChoiceSegment = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoiceSegment.setGeometry(QtCore.QRect(640, 440, 101, 20))
        self.pushButtonChoiceSegment.setStyleSheet("background-color: rgb(177, 177, 177);")
        self.pushButtonChoiceSegment.setObjectName("pushButtonChoiceSegment")
        imageSegmentationWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(imageSegmentationWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 809, 26))
        self.menubar.setObjectName("menubar")
        imageSegmentationWindow.setMenuBar(self.menubar)
        self.statusbarImageSegmentation = QtWidgets.QStatusBar(imageSegmentationWindow)
        self.statusbarImageSegmentation.setObjectName("statusbarImageSegmentation")
        imageSegmentationWindow.setStatusBar(self.statusbarImageSegmentation)

        self.retranslateUi(imageSegmentationWindow)
        QtCore.QMetaObject.connectSlotsByName(imageSegmentationWindow)

    def retranslateUi(self, imageSegmentationWindow):
        _translate = QtCore.QCoreApplication.translate
        imageSegmentationWindow.setWindowTitle(_translate("imageSegmentationWindow", "图像分割"))
        self.label.setText(_translate("imageSegmentationWindow", "1、由于照片的差异，需要手动调整一些参数，帮助系统更好的运行。\n"
"2、gaussBlur会去除照片的噪声点\n"
"3、强度梯度小于minThresh的必定不是边缘\n"
"4、强度梯度大于maxThresh的必定是边缘\n"
"5、kernel卷积核大小\n"
"5、dilate会连接不连续部分\n"
"6、强度梯度小于minChoice的必定不是边缘\n"
"8、强度梯度大于maxChoice的必定是边缘\n"
"9、kerChoice选项部分卷积核\n"
"10、dilChoice会连接选项部分不连续部分\n"
"11、eroChoice会丢弃部分边缘像素，可能会造成不连续\n"
"12、请随机选择一批图片中的一张\n"
"13、点击Esc退出settings界面\n"
""))
        self.pushButtonImageSegmentation.setText(_translate("imageSegmentationWindow", "点击开始"))
        self.pushButtonChoiceSegment.setText(_translate("imageSegmentationWindow", "选择图片"))
