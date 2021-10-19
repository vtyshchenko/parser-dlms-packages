from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication, QTreeWidgetItem
from os.path import abspath, join

from view.ui.ui_main import Ui_MainWindow
from controller.__json import Json

from component.gurux_dlms.enums.DataType import DataType
from component.gurux_dlms.enums.ObjectType import ObjectType
from component.gurux_dlms.GXDLMSClient import GXDLMSClient

from controller.parse_packages import ParsePackage


class MainView(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainView, self).__init__(parent)
        self.setupUi(self)

        self.json = Json()
        self.GXDLMSClient = GXDLMSClient()

        self.actionLoad.triggered.connect(self.load)
        self.actionSave.triggered.connect(self.save)
        self.actionExit.triggered.connect(self.exit)
        self.actionCopy.triggered.connect(self.copy)
        self.actionAnalize.triggered.connect(self.analyze)
        self.actionHelp.triggered.connect(self.help)
        self.actionAbout.triggered.connect(self.about)
        self.tabs.currentChanged.connect(self.tab_changed)

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

        self.enabled_actions(False)
        self.actionLoad.setEnabled(self.tabs.currentIndex() == 1)

        self.prgrsbrPackagesParse.setValue(0)

        # self.data = None
        self.data_dict = dict()
        self.parse_package = ParsePackage()

        self.object_type = dict()
        for obj_type in list(ObjectType):
            self.object_type[obj_type.value] = obj_type.name

        self.data_type = dict()
        for data_type in list(DataType):
            self.data_type[data_type.value] = data_type.name

    def tab_changed(self):
        # self.enabled_actions(False)
        self.actionLoad.setEnabled(self.tabs.currentIndex() == 1)

    def enabled_actions(self, value):
        self.actionLoad.setEnabled(value)
        self.actionSave.setEnabled(value)
        # self.actionCopy.setEnabled(value)
        # self.actionAnalize.setEnabled(value)

    def load(self):
        """ Documentation for a method load. Added:
        closes the main window
        """
        self.parse_package.data_packages = dict()
        self.enabled_actions(False)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt)", options=options)
        if fileName:
            file_data = open(fileName, 'r')
            with file_data:
                data = file_data.read()
                self.txtedtPackages.setText(data)
            self.prgrsbrPackagesParse.setMaximum(len(data))

            pos = 0
            i = 0
            idx = 0
            idx2 = 0
            while idx != -1 and data[pos:] != '':
                idx = pos + data[pos:].find('7E')
                if (idx-idx2) == 0:
                    break
                idx2 = idx + data[idx+1:].find('\n') + 1
                self.parse_package.data_packages[i] = data[idx:idx2]

                pos = idx2 + 1
                self.prgrsbrPackagesParse.setValue(pos)
                QApplication.processEvents()
                i += 1

        self.prgrsbrPackagesParse.setValue(len(data))
        self.parse_package.parse_packages()
        self.data_dict = self.parse_package.data_dict
        self.enabled_actions(True)

    def save(self):
        """ Documentation for a method save. Added:
        closes the main window
        """
        save_dir = join(abspath('.'), 'results')

        file_saved_name, aaa = QFileDialog.getSaveFileName(
            caption="Save result",
            directory=save_dir,
            filter="*.json"
        )
        if file_saved_name.find('.json') == -1:
            file_saved_name += '.json'

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
                                                  "All Files (*.json)", options=options)
        if fileName:
            data = self.json.load_file(fileName)
            self.txtedtPackages.setText(f"{data}")

    def analyze(self):
        """ Documentation for a method analyze. Added:
        closes the main window
        """
        if len(self.data_dict) == 0:
            self.data_dict["0"] = {"data": {"package": self.plntxtedtPackage.toPlainText()}}
        self.parse_package.parse_package()
        self.show_result()
        self.data_dict = dict()

    def show_result(self):
        self.trwdtResult.clear()
        items = []
        for key, values in self.data_dict["0"].items():
            item = QTreeWidgetItem([key])
            if isinstance(values, dict):
                for k, v in values.items():
                    it = QTreeWidgetItem([k])
                    child = QTreeWidgetItem([k, f"{v}"])
                    it.addChild(child)
                    item.addChild(it)
            else:
                child = QTreeWidgetItem([key, f"{values}"])
                item.addChild(child)
            items.append(item)

        self.trwdtResult.insertTopLevelItems(0, items)

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
