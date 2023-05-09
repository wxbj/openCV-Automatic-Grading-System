import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.initialWindow import Ui_initialWindow
from ui.inputAnswerWindow import Ui_inputAnswerWindow
from ui.inputReplyWindow import Ui_inputReplyWindow
from ui.gradingPaperWondow import Ui_gradingPaperWindow
from ui.menuWindow import Ui_menuWindow


class menuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_menuWindow()
        initialWindow = Ui_initialWindow()
        inputAnswerWindow = Ui_inputAnswerWindow()
        inputReplyWindow = Ui_inputReplyWindow()
        gradingPaperWindow = Ui_gradingPaperWindow()
        self.ui.setupUi(self)
        self.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = menuWindow()
    sys.exit(app.exec_())
