import sys

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem

from main.imageProcess import getAnswer
from ui.initialWindow import Ui_initialWindow
from ui.inputAnswerWindow import Ui_inputAnswerWindow
from ui.inputReplyWindow import Ui_inputReplyWindow
from ui.gradingPaperWondow import Ui_gradingPaperWindow
from ui.menuWindow import Ui_menuWindow
from utils.windowUtil import *

answer = {}
replys = {}
replyUrls = []
gradings = []


class initialWindow(QMainWindow, Ui_initialWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class inputAnswerWindow(QMainWindow, Ui_inputAnswerWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonChoice.clicked.connect(self.choiceAddress)

    def choiceAddress(self):
        fileAddress = QFileDialog.getOpenFileName(self, '选择文件',
                                                  'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System\img',
                                                  "Image files (*.jpg *.gif *.png)")[0]
        self.lineEditAddress.setText(fileAddress)
        global answer
        answer = getAnswer(fileAddress)
        answerStr = ""
        for key, value in answer.items():
            answerStr += key
            for i in value:
                answerStr += str(i)
                answerStr += ' '
            answerStr += "\n"
        self.textEditAnswer.setText(answerStr)


class inputReplyWindow(QMainWindow, Ui_inputReplyWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonReply.clicked.connect(self.getFileUrls)

    def getFileUrls(self):
        global replyUrls
        replyUrls = QFileDialog.getOpenFileNames(self, '选择文件',
                                                 'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System\img',
                                                 "Image files (*.jpg *.gif *.png)")[0]
        replyStr = ""
        for i in replyUrls:
            replyStr = replyStr + i + "\n"
        self.textEditReply.setText(replyStr)


class gradingPaperWindow(QMainWindow, Ui_gradingPaperWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.controller()

    def controller(self):
        global gradings
        gradings = getGradingLists(answer, replys)

        for grading in gradings:
            row = self.tableWidgetGrading.rowCount()
            self.tableWidgetGrading.insertRow(row)
            for j in range(len(grading)):
                item = QTableWidgetItem(str(grading[j]))
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidgetGrading.setItem(row, j, item)


class menuWindow(QMainWindow, Ui_menuWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.inputAnswerWindow = inputAnswerWindow()
        self.initialWindow = initialWindow()
        self.inputReplyWindow = inputReplyWindow()
        self.gradingPaperWindow = gradingPaperWindow()

        number = self.stackedWidget.addWidget(self.initialWindow)
        self.stackedWidget.setCurrentIndex(number)

        self.controller()
        self.show()

    def controller(self):
        self.actionInputAnswer.triggered.connect(self.inputAnswer)
        self.actionInputReply.triggered.connect(self.inputReply)
        self.actionGradingPaper.triggered.connect(self.gradingPaper)

    def inputAnswer(self):
        number = self.stackedWidget.addWidget(self.inputAnswerWindow)
        self.stackedWidget.setCurrentIndex(number)

    def inputReply(self):
        number = self.stackedWidget.addWidget(self.inputReplyWindow)
        self.stackedWidget.setCurrentIndex(number)

    def gradingPaper(self):
        number = self.stackedWidget.addWidget(self.gradingPaperWindow)
        self.stackedWidget.setCurrentIndex(number)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = menuWindow()
    sys.exit(app.exec_())
