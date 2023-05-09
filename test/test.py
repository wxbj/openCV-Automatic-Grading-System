import sys

from PyQt5.QtWidgets import QApplication, QMainWindow

from ui.initialWindow import Ui_initialWindow
from ui.initialWindow import Ui_initialWindow
from ui.initialWindow import Ui_initialWindow
from ui.initialWindow import Ui_initialWindow


class menuWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui =
        self.ui.setupUi(self)
        # 调用监听函数
        self.controller()
        self.show()

    # 监听事件都放在这里面
    def controller(self):
        self.ui.actionInputAnswer.triggered.connect(self.actionInputAnswer)

    def actionInputAnswer(self):
        self.ui.lableResult.setText("答案")
        self.ui.statusbar.showMessage("读入成功")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = menuWindow()
    sys.exit(app.exec_())
