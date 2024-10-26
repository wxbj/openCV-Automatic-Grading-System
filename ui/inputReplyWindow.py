from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_inputReplyWindow(object):
    def setupUi(self, inputReplyWindow):
        inputReplyWindow.setObjectName("inputReplyWindow")
        inputReplyWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(inputReplyWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonReply = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonReply.setGeometry(QtCore.QRect(640, 30, 93, 28))
        self.pushButtonReply.setObjectName("pushButtonReply")
        self.textEditReply = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditReply.setGeometry(QtCore.QRect(20, 70, 751, 471))
        self.textEditReply.setObjectName("textEditReply")
        inputReplyWindow.setCentralWidget(self.centralwidget)
        self.statusBarInputReply = QtWidgets.QStatusBar(inputReplyWindow)
        self.statusBarInputReply.setObjectName("statusBarInputReply")
        inputReplyWindow.setStatusBar(self.statusBarInputReply)

        self.retranslateUi(inputReplyWindow)
        QtCore.QMetaObject.connectSlotsByName(inputReplyWindow)

    def retranslateUi(self, inputReplyWindow):
        _translate = QtCore.QCoreApplication.translate
        inputReplyWindow.setWindowTitle(_translate("inputReplyWindow", "试卷读入"))
        self.pushButtonReply.setText(_translate("inputReplyWindow", "选择试卷"))
