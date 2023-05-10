import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.initialWindow import Ui_initialWindow
from ui.inputAnswerWindow import Ui_inputAnswerWindow
from ui.inputReplyWindow import Ui_inputReplyWindow
from ui.gradingPaperWondow import Ui_gradingPaperWindow
from ui.menuWindow import Ui_menuWindow


class initialWindow(QMainWindow, Ui_initialWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class inputAnswerWindow(QMainWindow, Ui_inputAnswerWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class inputReplyWindow(QMainWindow, Ui_inputReplyWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


class gradingPaperWindow(QMainWindow, Ui_gradingPaperWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)


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
