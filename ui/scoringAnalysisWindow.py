from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_scoringAnalysisWindow(object):
    def setupUi(self, scoringAnalysisWindow):
        scoringAnalysisWindow.setObjectName("scoringAnalysisWindow")
        scoringAnalysisWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(scoringAnalysisWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButtonStart = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStart.setGeometry(QtCore.QRect(640, 30, 93, 28))
        self.pushButtonStart.setObjectName("pushButtonStart")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(3, 86, 791, 461))
        self.textEdit.setObjectName("textEdit")
        scoringAnalysisWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(scoringAnalysisWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        scoringAnalysisWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(scoringAnalysisWindow)
        self.statusbar.setObjectName("statusbar")
        scoringAnalysisWindow.setStatusBar(self.statusbar)

        self.retranslateUi(scoringAnalysisWindow)
        QtCore.QMetaObject.connectSlotsByName(scoringAnalysisWindow)

    def retranslateUi(self, scoringAnalysisWindow):
        _translate = QtCore.QCoreApplication.translate
        scoringAnalysisWindow.setWindowTitle(_translate("scoringAnalysisWindow", "成绩分析"))
        self.pushButtonStart.setText(_translate("scoringAnalysisWindow", "开始分析"))
