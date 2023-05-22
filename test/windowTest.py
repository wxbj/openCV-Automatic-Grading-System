import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QTableView, QLabel

from ui.initialWindow import Ui_initialWindow
from ui.inputAnswerWindow import Ui_inputAnswerWindow
from ui.inputReplyWindow import Ui_inputReplyWindow
from ui.gradingPaperWondow import Ui_gradingPaperWindow
from ui.blurImageProcessingWindow import Ui_blurImageProcessingWindow
from ui.menuWindow import Ui_menuWindow
from ui.basicParameterSettingsWindow import Ui_basicParameterSettingsWindow
from test.windowUtilTest import *

answer = {}  # 存放答案列表
replyUrls = []  # 存放学生列表
gradings = []  # 存放学生成绩


# 初始界面，用于用户登录的显示内容
class initialWindow(QMainWindow, Ui_initialWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 设定基本参数
class basicParameterSettingsWindow(QMainWindow, Ui_basicParameterSettingsWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.fileAddress = ''
        self.pushButtonBasicParameterChoice.clicked.connect(self.basicParameterAddress)
        self.pushButtonStartAdjust.clicked.connect(self.startAdjust)

    def basicParameterAddress(self):
        self.fileAddress = QFileDialog.getOpenFileName(self, '选择文件',
                                                       'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System\img',
                                                       "Image files (*.jpg *.gif *.png)")[0]
        self.lineEditBasicParameterAddress.setText(self.fileAddress)

    def startAdjust(self):
        filePath = getBasicParameter(self.fileAddress)

        self.labelBasicParameterImage.setPixmap(QtGui.QPixmap(filePath))
        self.labelBasicParameterImage.setScaledContents(True)


# 从图片读入答案
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
        keys = ["考试科目栏:", "选择第一栏:", "选择第二栏:", "选择第三栏:", "选择第四栏:"]
        for key, value in answer.items():
            if key in keys:
                answerStr += key
                for i in value:
                    answerStr += str(i)
                    answerStr += ' '
                answerStr += "\n"
        self.textEditAnswer.setText(answerStr)


# 从文件夹读入试卷
class inputReplyWindow(QMainWindow, Ui_inputReplyWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonReply.clicked.connect(self.getFileUrls)

    def getFileUrls(self):
        replyFolderUrl = QFileDialog.getExistingDirectory(self, '选择文件夹',
                                                          'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System\img')
        replyNames = os.listdir(replyFolderUrl)

        global replyUrls
        for i in replyNames:
            replyUrls.append(replyFolderUrl + "/" + i)

        replyStr = ""
        for i in replyNames:
            replyStr = replyStr + replyFolderUrl + "/" + i + "\n"
        self.textEditReply.setText(replyStr)


# 评分
class gradingPaperWindow(QMainWindow, Ui_gradingPaperWindow, QTableView):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonGrading.clicked.connect(self.getGrading)

    def getGrading(self):
        global answer
        global replyUrls
        global gradings
        gradings = getGradingLists(answer, replyUrls)
        for grading in gradings:
            row = self.tableWidgetGrading.rowCount()
            self.tableWidgetGrading.insertRow(row)
            for j in range(len(grading)):
                item = QTableWidgetItem(str(grading[j]))
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidgetGrading.setItem(row, j, item)


# 模糊图像处理
class blurImageProcessingWindow(QMainWindow, Ui_blurImageProcessingWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 菜单栏
class menuWindow(QMainWindow, Ui_menuWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.initialWindow = initialWindow()
        self.inputAnswerWindow = inputAnswerWindow()
        self.inputReplyWindow = inputReplyWindow()
        self.gradingPaperWindow = gradingPaperWindow()
        self.blurImageProcessingWindow = blurImageProcessingWindow()
        self.basicParameterSettingsWindow = basicParameterSettingsWindow()

        number = self.stackedWidget.addWidget(self.initialWindow)
        self.stackedWidget.setCurrentIndex(number)

        self.controller()
        self.show()

    def controller(self):
        self.actionInputAnswer.triggered.connect(self.inputAnswer)
        self.actionInputReply.triggered.connect(self.inputReply)
        self.actionGradingPaper.triggered.connect(self.gradingPaper)
        self.actionOutputExcel.triggered.connect(self.outputExcel)
        self.menuBlurImageProcessing.triggered.connect(self.blurImageProcessing)
        self.actionBasicParameterSettings.triggered.connect(self.basicParameterSettings)

    def inputAnswer(self):
        number = self.stackedWidget.addWidget(self.inputAnswerWindow)
        self.stackedWidget.setCurrentIndex(number)

    def inputReply(self):
        number = self.stackedWidget.addWidget(self.inputReplyWindow)
        self.stackedWidget.setCurrentIndex(number)

    def gradingPaper(self):
        number = self.stackedWidget.addWidget(self.gradingPaperWindow)
        self.stackedWidget.setCurrentIndex(number)

    def outputExcel(self):
        global gradings
        writeGradExcel(gradings)
        self.statusbar.showMessage("保存成功！")

    def blurImageProcessing(self):
        number = self.stackedWidget.addWidget(self.blurImageProcessingWindow)
        self.stackedWidget.setCurrentIndex(number)

    def basicParameterSettings(self):
        number = self.stackedWidget.addWidget(self.basicParameterSettingsWindow)
        self.stackedWidget.setCurrentIndex(number)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = menuWindow()
    sys.exit(app.exec_())
