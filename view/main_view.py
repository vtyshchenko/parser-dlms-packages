# from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow

from view.ui.ui_main import MainWindow


class MainView(QMainWindow, MainWindow):
    def __init__(self, parent=None, user_name=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)
