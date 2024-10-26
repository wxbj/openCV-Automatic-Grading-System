from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_displayPictureWindow(object):
    def setupUi(self, displayPictureWindow):
        displayPictureWindow.setObjectName("displayPictureWindow")
        displayPictureWindow.resize(800, 628)
        self.centralwidget = QtWidgets.QWidget(displayPictureWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEditFileUrl = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditFileUrl.setGeometry(QtCore.QRect(10, 20, 661, 31))
        self.textEditFileUrl.setObjectName("textEditFileUrl")
        self.pushButtonChoiceFolder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoiceFolder.setGeometry(QtCore.QRect(680, 20, 101, 28))
        self.pushButtonChoiceFolder.setObjectName("pushButtonChoiceFolder")
        self.labelPicture = QtWidgets.QLabel(self.centralwidget)
        self.labelPicture.setGeometry(QtCore.QRect(190, 60, 360, 480))
        self.labelPicture.setText("")
        self.labelPicture.setObjectName("labelPicture")
        self.pushButtonPrevious = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrevious.setGeometry(QtCore.QRect(80, 550, 93, 28))
        self.pushButtonPrevious.setObjectName("pushButtonPrevious")
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNext.setGeometry(QtCore.QRect(570, 550, 93, 28))
        self.pushButtonNext.setObjectName("pushButtonNext")
        displayPictureWindow.setCentralWidget(self.centralwidget)
        self.statusBarDisplayPicture = QtWidgets.QStatusBar(displayPictureWindow)
        self.statusBarDisplayPicture.setObjectName("statusBarDisplayPicture")
        displayPictureWindow.setStatusBar(self.statusBarDisplayPicture)

        self.retranslateUi(displayPictureWindow)
        QtCore.QMetaObject.connectSlotsByName(displayPictureWindow)

    def retranslateUi(self, displayPictureWindow):
        _translate = QtCore.QCoreApplication.translate
        displayPictureWindow.setWindowTitle(_translate("displayPictureWindow", "图片浏览"))
        self.pushButtonChoiceFolder.setText(_translate("displayPictureWindow", "选择文件夹"))
        self.pushButtonPrevious.setText(_translate("displayPictureWindow", "上一张"))
        self.pushButtonNext.setText(_translate("displayPictureWindow", "下一张"))
