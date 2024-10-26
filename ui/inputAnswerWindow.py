from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_inputAnswerWindow(object):
    def setupUi(self, inputAnswerWindow):
        inputAnswerWindow.setObjectName("inputAnswerWindow")
        inputAnswerWindow.resize(800, 614)
        self.centralwidget = QtWidgets.QWidget(inputAnswerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonChoice = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoice.setGeometry(QtCore.QRect(650, 30, 101, 20))
        self.pushButtonChoice.setStyleSheet("background-color: rgb(177, 177, 177);")
        self.pushButtonChoice.setObjectName("pushButtonChoice")
        self.lineEditAddress = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditAddress.setGeometry(QtCore.QRect(40, 30, 591, 21))
        self.lineEditAddress.setObjectName("lineEditAddress")
        self.textEditAnswer = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditAnswer.setGeometry(QtCore.QRect(30, 110, 281, 451))
        self.textEditAnswer.setObjectName("textEditAnswer")
        self.pushButtonInputAnswer = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonInputAnswer.setGeometry(QtCore.QRect(120, 70, 93, 28))
        self.pushButtonInputAnswer.setObjectName("pushButtonInputAnswer")
        self.labelInputAnswerImage = QtWidgets.QLabel(self.centralwidget)
        self.labelInputAnswerImage.setGeometry(QtCore.QRect(370, 80, 360, 480))
        self.labelInputAnswerImage.setStyleSheet("# labelBasicParameterImage{\n"
"rgb(255, 255, 127)}")
        self.labelInputAnswerImage.setText("")
        self.labelInputAnswerImage.setObjectName("labelInputAnswerImage")
        inputAnswerWindow.setCentralWidget(self.centralwidget)
        self.statusBarInputAnswer = QtWidgets.QStatusBar(inputAnswerWindow)
        self.statusBarInputAnswer.setObjectName("statusBarInputAnswer")
        inputAnswerWindow.setStatusBar(self.statusBarInputAnswer)

        self.retranslateUi(inputAnswerWindow)
        QtCore.QMetaObject.connectSlotsByName(inputAnswerWindow)

    def retranslateUi(self, inputAnswerWindow):
        _translate = QtCore.QCoreApplication.translate
        inputAnswerWindow.setWindowTitle(_translate("inputAnswerWindow", "答案读入"))
        self.pushButtonChoice.setText(_translate("inputAnswerWindow", "选择答案图片"))
        self.pushButtonInputAnswer.setText(_translate("inputAnswerWindow", "提取答案"))
