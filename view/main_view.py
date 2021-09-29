# from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QMainWindow, QFileDialog
from os.path import abspath, join

from view.ui.ui_main import Ui_MainWindow
from controller.__json import Json

from component.gurux_dlms.enums.DataType import DataType
from component.gurux_dlms.enums.ErrorCode import ErrorCode
from component.gurux_dlms.enums.ObjectType import ObjectType
from component.gurux_dlms.enums.Unit import Unit
from component.gurux_dlms.internal._GXCommon import _GXCommon
from component.gurux_dlms.GXByteBuffer import GXByteBuffer


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

        self.object_type = dict()
        for obj_type in list(ObjectType):
            self.object_type[obj_type.value] = obj_type.name

        self.data_type = dict()
        for data_type in list(DataType):
            self.data_type[data_type.value] = data_type.name

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
                # bytes = GXByteBuffer(data)
                # <component.gurux_dlms.GXByteBuffer.GXByteBuffer object at 0x7f1e78b96b00>

                # bytes.array()
                # bytearray(b'~\xa0\x1c\x02!\x052\x85\xb8\xe6\xe6\x00\xc1\x01\xc1\x00p\x00\x00\x13\n\x02\xff\x03\x00\x16\x00o\x13~')
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
        self.parse_dlms()
        # for key in self.data.keys():
        #     tmp_data = self.data[key]

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

    def get_addr(self, idx, data):
        """ Documentation for a method get_addr. Added: 29.09.21 23:59 volodymyr.tyshchenko


        :param idx:
        :type idx:
        """
        is_end = '0'
        addr = list()
        i = idx
        while is_end == '0':
            is_end = bin(data[i])[-1]
            addr.append(data[i])
            i += 1
        return (addr, i)

    def parse_dlms(self):
        """ Documentation for a method parseDLMS. Added: 29.09.21 20:52 volodymyr.tyshchenko
        parse DLMS packages
        """
        for key, obj in self.data_dict.items():
            pack = GXByteBuffer(obj["package"]).array()
            self.data_dict[key]["data"] = dict()
            self.data_dict[key]["data"]["Length"] = pack[2]

            self.data_dict[key]["data"]["addr_from"], i = self.get_addr(idx=3, data=pack)
            self.data_dict[key]["data"]["addr_to"], i = self.get_addr(idx=i, data=pack)
            self.data_dict[key]["data"]["next"] = pack[i]
            self.data_dict[key]["data"]["pack_type"] = pack[i + 6]
            if pack[i + 6] == 0xC5:
                self.data_dict[key]["data"]["result"] = pack[i + 9]
            elif pack[i + 6] == 0xC4:
                self.data_dict[key]["data"]["result"] = pack[i + 9]
                self.data_dict[key]["data"]["type"] = {"value": pack[i + 10], "name": self.data_type[pack[i + 10]]}
                data = list()
                for j in range(i+11, len(pack)-3):
                    data.append(pack[j])
                self.data_dict[key]["data"]["value"] = data
            elif pack[i + 6] == 0xC0:
                self.data_dict[key]["data"]["type"] = {"value": pack[i + 10], "name": self.object_type[pack[i + 10]]}
                obis = f"{pack[i + 11]}.{pack[i + 12]}.{pack[i + 13]}.{pack[i + 14]}.{pack[i + 15]}.{pack[i + 16]}"
                self.data_dict[key]["data"]["obis"] = obis
                self.data_dict[key]["data"]["attribute"] = pack[i + 17]

        self.save()
