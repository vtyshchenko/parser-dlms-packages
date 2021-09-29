# from PyQt5.QtCore import Qt
import json

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from os.path import abspath, join, isfile

from view.ui.ui_main import Ui_MainWindow
from controller.__json import Json


class MainView(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)

        self.json = Json()

        self.actionLoad.triggered.connect(self.load)
        self.actionSave.triggered.connect(self.save)
        self.actionExit.triggered.connect(self.exit)
        self.actionCopy.triggered.connect(self.copy)
        self.actionAnalize.triggered.connect(self.analyze)
        self.actionHelp.triggered.connect(self.help)
        self.actionAbout.triggered.connect(self.about)

        self.tlbrOperations.addAction(self.actionLoad)
        self.tlbrOperations.addAction(self.actionSave)
        self.tlbrOperations.addSeparator()
        self.tlbrOperations.addAction(self.actionAnalize)
        self.tlbrOperations.addAction(self.actionCopy)
        self.tlbrOperations.addSeparator()
        self.tlbrOperations.addAction(self.actionHelp)
        self.tlbrOperations.addAction(self.actionAbout)
        self.tlbrOperations.addSeparator()
        self.tlbrOperations.addAction(self.actionExit)
        self.data = None
        self.data_dict = dict()

    def load(self):
        """ Documentation for a method load. Added:
        closes the main window
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt)", options=options)
        if fileName:
            file_data = open(fileName, 'r')
            with file_data:
                self.data = file_data.read()
                self.txtedtPackages.setText(self.data)

            i = 0
            idx = 0
            while self.data and idx != -1:
                idx = self.data.find('7E')
                idx2 = idx + self.data[idx+1:].find('\n') + 1
                data = self.data[idx:idx2]
                package = dict()
                package["package"] = data
                self.data_dict[i] = package
                self.data = self.data[idx2+1:]
                i += 1

    def save(self):
        """ Documentation for a method save. Added:
        closes the main window
        """
        save_dir = join(abspath('.'), 'results')

        file_saved_name, _ = QFileDialog.getSaveFileName(
            caption="Save result",
            directory=save_dir,
            filter="All Files (*.txt)"
        )

        self.json.save_file(file_saved_name, self.data_dict)

    def exit(self):
        """ Documentation for a method exit. Added:
        closes the main window
        """
        self.close()

    def copy(self):
        """ Documentation for a method copy. Added:
        closes the main window
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt)", options=options)
        if fileName:
            self.data = self.json.load_file(fileName)
            self.txtedtPackages.setText(f"{self.data}")

    def analyze(self):
        """ Documentation for a method analyze. Added:
        closes the main window
        """
        for key in self.data.keys():
            tmp_data = self.data[key]

    def help(self):
        """ Documentation for a method help. Added:
        closes the main window
        """
        pass

    def about(self):
        """ Documentation for a method about. Added:
        closes the main window
        """
        pass
