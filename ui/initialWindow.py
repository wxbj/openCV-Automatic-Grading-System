from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_initialWindow(object):
    def setupUi(self, initialWindow):
        initialWindow.setObjectName("initialWindow")
        initialWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(initialWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.labelInitialText = QtWidgets.QLabel(self.centralwidget)
        self.labelInitialText.setGeometry(QtCore.QRect(1, 4, 791, 581))
        self.labelInitialText.setStyleSheet("#labelInitialText{\n"
"font: 18pt \"宋体\";\n"
"\n"
"}\n"
"")
        self.labelInitialText.setObjectName("labelInitialText")
        initialWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(initialWindow)
        QtCore.QMetaObject.connectSlotsByName(initialWindow)

    def retranslateUi(self, initialWindow):
        _translate = QtCore.QCoreApplication.translate
        initialWindow.setWindowTitle(_translate("initialWindow", "初始界面"))
        self.labelInitialText.setText(_translate("initialWindow", "优美胜于丑陋\n"
"明了胜于晦涩\n"
"简洁胜于复杂\n"
"复杂胜于凌乱\n"
"扁平胜于嵌套\n"
"间隔胜于紧凑\n"
"可读性很重要\n"
"即便假借特例的实用性之名，也不可违背这些规则\n"
"不要包容所有错误，除非你确定需要这样做\n"
"当存在多种可能，不要尝试去猜测\n"
"而是尽量找一种，最好是唯一一种明显的解决方案\n"
"虽然这并不容易，因为你不是 Python 之父\n"
"做也许好过不做，但不假思索就动手还不如不做\n"
"如果你无法向人描述你的方案，那肯定不是一个好方案；反之亦然\n"
"命名空间是一种绝妙的理念，我们应当多加利用\n"
""))
