from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_preprocessingPapersWindow(object):
    def setupUi(self, preprocessingPapersWindow):
        preprocessingPapersWindow.setObjectName("preprocessingPapersWindow")
        preprocessingPapersWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(preprocessingPapersWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.textEditPreprocessingFolder = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPreprocessingFolder.setGeometry(QtCore.QRect(30, 30, 591, 31))
        self.textEditPreprocessingFolder.setObjectName("textEditPreprocessingFolder")
        self.pushButtonChoiceFolder = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonChoiceFolder.setGeometry(QtCore.QRect(640, 30, 131, 28))
        self.pushButtonChoiceFolder.setObjectName("pushButtonChoiceFolder")
        self.textEditPreprocessingFileList = QtWidgets.QTextEdit(self.centralwidget)
        self.textEditPreprocessingFileList.setGeometry(QtCore.QRect(30, 80, 741, 351))
        self.textEditPreprocessingFileList.setObjectName("textEditPreprocessingFileList")
        self.pushButtonStartHandle = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonStartHandle.setGeometry(QtCore.QRect(110, 490, 93, 28))
        self.pushButtonStartHandle.setObjectName("pushButtonStartHandle")
        self.pushButtonSaveResult = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonSaveResult.setGeometry(QtCore.QRect(500, 500, 93, 28))
        self.pushButtonSaveResult.setObjectName("pushButtonSaveResult")
        preprocessingPapersWindow.setCentralWidget(self.centralwidget)
        self.statusBarPreprocessing = QtWidgets.QStatusBar(preprocessingPapersWindow)
        self.statusBarPreprocessing.setObjectName("statusBarPreprocessing")
        preprocessingPapersWindow.setStatusBar(self.statusBarPreprocessing)

        self.retranslateUi(preprocessingPapersWindow)
        QtCore.QMetaObject.connectSlotsByName(preprocessingPapersWindow)

    def retranslateUi(self, preprocessingPapersWindow):
        _translate = QtCore.QCoreApplication.translate
        preprocessingPapersWindow.setWindowTitle(_translate("preprocessingPapersWindow", "预处理试卷"))
        self.pushButtonChoiceFolder.setText(_translate("preprocessingPapersWindow", "选择试卷文件夹"))
        self.pushButtonStartHandle.setText(_translate("preprocessingPapersWindow", "开始处理"))
        self.pushButtonSaveResult.setText(_translate("preprocessingPapersWindow", "保存结果"))
