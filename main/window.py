import os

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QTableWidgetItem, QTableView, QLabel, QInputDialog, \
    QLineEdit

from ui.initialWindow import Ui_initialWindow
from ui.inputAnswerWindow import Ui_inputAnswerWindow
from ui.inputReplyWindow import Ui_inputReplyWindow
from ui.gradingPaperWondow import Ui_gradingPaperWindow
from ui.menuWindow import Ui_menuWindow
from ui.perspectiveTransformationWindow import Ui_perspectiveTransformationWindow
from ui.preprocessingPapersWindow import Ui_preprocessingPapersWindow
from ui.displayPicture import Ui_displayPictureWindow
from ui.examPaperSettingWindow import Ui_examPaperSettingWindow

from utils.windowUtil import *
from main.imageTransformation import getBasicParameter
from main.optionDetection import getAnswer

basicSettings = [106, 74, 2, 1]  # 存放图片透视变换需要的参数
preprocessedFolder = ''  # 预处理完成的试卷夹
answer = {}  # 存放答案列表
replyUrls = []  # 存放学生列表
gradings = []  # 存放学生成绩
paperOption = {}  # 设卷格式


# 图片浏览
class displayPictureWindow(QMainWindow, Ui_displayPictureWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.choiceFolderUrl = ""  # 用户选择的文件夹
        self.number = 0  # 当前显示的图片编号

        self.pushButtonChoiceFolder.clicked.connect(self.choiceFolder)
        self.pushButtonPrevious.clicked.connect(self.previous)
        self.pushButtonNext.clicked.connect(self.next)

    def choiceFolder(self):
        try:
            self.choiceFolderUrl = QFileDialog.getExistingDirectory(self, '选择文件夹',
                                                                    'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System\img')

            solveAutomaticRotationOfImage(self.choiceFolderUrl)
            self.showQPixmap()
        except:
            self.statusBarDisplayPicture.showMessage("未选择图片文件夹")

    def previous(self):
        try:
            if self.number == 0:
                self.number = len(os.listdir(self.choiceFolderUrl)) - 1
            else:
                self.number -= 1
            self.showQPixmap()
        except:
            self.statusBarDisplayPicture.showMessage("未选择图片文件夹")

    def next(self):
        try:
            if self.number == (len(os.listdir(self.choiceFolderUrl)) - 1):
                self.number = 0
            else:
                self.number += 1
            self.showQPixmap()
        except:
            self.statusBarDisplayPicture.showMessage("未选择图片文件夹")

    # 工具方法，用于显示文件路径和图片
    def showQPixmap(self):
        self.textEditFileUrl.setText(self.choiceFolderUrl + "\\" + os.listdir(self.choiceFolderUrl)[self.number])
        self.labelPicture.setPixmap(
            QtGui.QPixmap(self.choiceFolderUrl + "\\" + os.listdir(self.choiceFolderUrl)[self.number]))
        self.labelPicture.setScaledContents(True)
        self.statusBarDisplayPicture.showMessage("")


# 初始界面，用于用户登录的显示内容
class initialWindow(QMainWindow, Ui_initialWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


# 预处理试卷界面
class preprocessingPapersWindow(QMainWindow, Ui_preprocessingPapersWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.preprocessingPapersUrls = []
        self.img = []

        self.pushButtonChoiceFolder.clicked.connect(self.getFileUrls)
        self.pushButtonStartHandle.clicked.connect(self.startHandle)
        self.pushButtonSaveResult.clicked.connect(self.saveResult)

    def getFileUrls(self):
        preprocessingPapersFolderUrl = QFileDialog.getExistingDirectory(self, '选择文件夹',
                                                                        'D:/BaiduSyncdisk/code/openCV-Automatic-Grading-System\img')
        self.textEditPreprocessingFolder.setText(preprocessingPapersFolderUrl)

        preprocessingPapersStr = ""
        for i in os.listdir(preprocessingPapersFolderUrl):
            self.preprocessingPapersUrls.append(preprocessingPapersFolderUrl + "/" + i)
            preprocessingPapersStr = preprocessingPapersStr + preprocessingPapersFolderUrl + "/" + i + "\n"

        self.textEditPreprocessingFileList.setText(preprocessingPapersStr)

    def startHandle(self):
        self.img = preprocessingPapers(self.preprocessingPapersUrls, basicSettings)
        self.statusBarPreprocessing.showMessage("处理完成")

    def saveResult(self):
        global preprocessedFolder
        preprocessedFolder = saveResultFolder(QInputDialog.getText(self, "输入框", "试卷放置的文件夹名:", QLineEdit.Normal, "")[0],
                                              self.img)
        self.statusBarPreprocessing.showMessage("保存完成")


# 设定基本参数
class perspectiveTransformationWindow(QMainWindow, Ui_perspectiveTransformationWindow):
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
        global basicSettings
        self.labelOriginalBasicParameterImage.setPixmap(QtGui.QPixmap(self.fileAddress))
        self.labelOriginalBasicParameterImage.setScaledContents(True)

        result = getBasicParameter(self.fileAddress)
        basicSettings = result[1]
        self.labelBasicParameterImage.setPixmap(QtGui.QPixmap(result[0]))
        self.labelBasicParameterImage.setScaledContents(True)
        os.remove(result[0])


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
        global paperOption
        answer = getAnswer(fileAddress, paperOption)
        answerStr = ""
        keys = ["考试科目栏:", "单选题:", "多选题:"]
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
        gradings = getGradingLists(answer, replyUrls, paperOption)
        print(gradings)
        for grading in gradings:
            row = self.tableWidgetGrading.rowCount()
            self.tableWidgetGrading.insertRow(row)
            for j in range(len(grading)):
                item = QTableWidgetItem(str(grading[j]))
                item.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
                self.tableWidgetGrading.setItem(row, j, item)


# 试卷设置
class examPaperSettingWindow(QMainWindow, Ui_examPaperSettingWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButtonAscertain.clicked.connect(self.ascertain)

    def ascertain(self):
        global paperOption
        paperOption["单选题开始"] = int(self.comboBoxSingleFirst.currentText())
        paperOption["单选题终止"] = int(self.comboBoxSingleSecond.currentText())
        paperOption["单选题分值"] = int(self.spinBoxSingleScore.value())
        paperOption["多选题开始"] = int(self.comboBoxMultFirst.currentText())
        paperOption["多选题终止"] = int(self.comboBoxMultSecond.currentText())
        paperOption["多选题分值"] = int(self.spinBoxMultScore.value())
        self.statusBarExamPaperSetting.showMessage("设置完成")


# 主界面
class menuWindow(QMainWindow, Ui_menuWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.initialWindow = initialWindow()
        self.inputAnswerWindow = inputAnswerWindow()
        self.inputReplyWindow = inputReplyWindow()
        self.gradingPaperWindow = gradingPaperWindow()
        self.perspectiveTransformationWindow = perspectiveTransformationWindow()
        self.preprocessingPapersWindow = preprocessingPapersWindow()
        self.displayPictureWindow = displayPictureWindow()
        self.examPaperSettingWindow = examPaperSettingWindow()

        number = self.stackedWidget.addWidget(self.initialWindow)
        self.stackedWidget.setCurrentIndex(number)

        self.controller()
        self.show()

    def controller(self):
        self.actionInputAnswer.triggered.connect(self.inputAnswer)
        self.actionInputReply.triggered.connect(self.inputReply)
        self.actionGradingPaper.triggered.connect(self.gradingPaper)
        self.actionOutputExcel.triggered.connect(self.outputExcel)
        self.actionPerspectiveTransformation.triggered.connect(self.perspectiveTransformation)
        self.actionPreprocessingPapers.triggered.connect(self.preprocessingPapers)
        self.actionDisplayPicture.triggered.connect(self.displayPicture)
        self.actionExamPaperSetting.triggered.connect(self.examPaperSetting)

    def inputAnswer(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.inputAnswerWindow))

    def inputReply(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.inputReplyWindow))

    def gradingPaper(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.gradingPaperWindow))

    def outputExcel(self):
        global gradings
        writeGradExcel(gradings)
        self.statusBar.showMessage("保存成功！")

    def perspectiveTransformation(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.perspectiveTransformationWindow))

    def preprocessingPapers(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.preprocessingPapersWindow))

    def displayPicture(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.displayPictureWindow))

    def examPaperSetting(self):
        self.stackedWidget.setCurrentIndex(self.stackedWidget.addWidget(self.examPaperSettingWindow))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = menuWindow()
    sys.exit(app.exec_())
