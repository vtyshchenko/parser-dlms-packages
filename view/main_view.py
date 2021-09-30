# from PyQt5.QtCore import Qt
from sys import excepthook
from time import time

from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
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
        self.data_packages = dict()
        self.data_dict = dict()

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
        self.actionCopy.setEnabled(value)
        self.actionAnalize.setEnabled(value)

    def parse_data_package(self):
        for key in sorted(list(self.data_packages)):
            obj = self.data_packages[key]
            self.data_dict[key] = dict()
            self.data_dict[key]["data"] = dict()
            self.data_dict[key]["data"]["package"] = obj
            try:
                pack = GXByteBuffer(obj).array()
            except Exception as exc:
                print(f"key = {key}\nobj = {obj}\nexc = {exc}")
                pack = GXByteBuffer().array()
            idx = 0
            for j in range(len(pack)):
                if pack[j] == 0xE6 and (pack[j + 1] == 0xE6 or pack[j + 1] == 0xE7):
                    idx = j + 3
                    break
            if len(pack) - 2 == pack[2]:
                body_idx = (idx + 4) * 3
                if pack[idx] == 0xC0:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                elif pack[idx] == 0xC1:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                elif pack[idx] == 0xC2:
                    pass
                elif pack[idx] == 0xC3:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                elif pack[idx] == 0xC4:
                    self.data_dict[key]["data"]["body"] = obj[body_idx:-3*3]
                    if pack[idx+1] == 0x02:
                        pass
                elif pack[idx] == 0xC5:
                    self.data_dict[key]["data"]["result"] = obj[body_idx:body_idx+3]
                    self.data_dict[key]["data"]["body"] = obj[body_idx:body_idx+3]
                elif pack[idx] == 0xC6:
                    pass
                elif pack[idx] == 0xC7:
                    self.data_dict[key]["data"]["result"] = obj[body_idx:body_idx+3]
                    self.data_dict[key]["data"]["body"] = obj[body_idx:body_idx+3]
            else:
                pass

    def load(self):
        """ Documentation for a method load. Added:
        closes the main window
        """
        self.enabled_actions(False)
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*.txt)", options=options)
        # ll = 0
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
            # ll = len(data)
            while idx != -1 and data[pos:] != '':
                # print(f"0 idx = {idx}, idx2 = {idx2}")
                idx = pos + data[pos:].find('7E')
                if (idx-idx2) == 0:
                    break
                idx2 = idx + data[idx+1:].find('\n') + 1
                # print(f"1 idx = {idx}, idx2 = {idx2}")
                self.data_packages[i] = data[idx:idx2]

                pos = idx2 + 1
                self.prgrsbrPackagesParse.setValue(pos)
                QApplication.processEvents()
                i += 1
        # print(f"{ll}")
        self.prgrsbrPackagesParse.setValue(len(data))
        self.parse_data_package()
        self.enabled_actions(True)

    def save(self):
        """ Documentation for a method save. Added:
        closes the main window
        """
        save_dir = join(abspath('.'), 'results')

        file_saved_name, _ = QFileDialog.getSaveFileName(
            caption="Save result",
            directory=save_dir,
            filter="All Files (*.json)"
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
                                                  "All Files (*.json)", options=options)
        if fileName:
            data = self.json.load_file(fileName)
            self.txtedtPackages.setText(f"{data}")

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

    @staticmethod
    def get_addr(idx: int, data: bytearray):
        """ Documentation for a method get_addr. Added: 29.09.21 23:59 volodymyr.tyshchenko

        :param idx: data element index
        :type idx: int
        :param data:
        :type data: bytearray

        :return address list and next element index in data
        :rtype tuple
        """
        is_end = '0'
        addr = list()
        i = idx
        while is_end == '0':
            is_end = bin(data[i])[-1]
            addr.append(data[i])
            i += 1
        return tuple([addr, i])

    def parse_dlms(self):
        """ Documentation for a method parseDLMS. Added: 29.09.21 20:52 volodymyr.tyshchenko
        parse DLMS packages
        """
        try:
            for key, obj in self.data_dict.items():
                is_c4_last = True
                pack = GXByteBuffer(obj["data"]["package"]).array()
                i = self.parse_head(pack=pack, key=key)
                if pack[i] == 0xC5:
                    self.data_dict[key]["result"] = pack[i + 3]
                elif pack[i] == 0xC4:
                    self.data_dict[key]["result"] = pack[i + 3]
                    self.data_dict[key]["type"] = {"value": pack[i + 4], "name": self.data_type[pack[i + 4]]}
                    data = list()
                    for j in range(i+5, len(pack)-3):
                        data.append(pack[j])
                    self.data_dict[key]["value"] = data
                elif pack[i] == 0xC0:
                    if key == 480:
                        print("")
                    if pack[i + 1] == 0x01:
                        self.data_dict[key]["type"] = {
                            "value": pack[i + 4], "name": self.object_type[pack[i + 4]]
                            }
                        obis = f"{pack[i + 5]}.{pack[i + 6]}.{pack[i + 7]}.{pack[i + 8]}.{pack[i + 9]}.{pack[i + 10]}"
                        self.data_dict[key]["obis"] = obis
                        self.data_dict[key]["attribute"] = pack[i + 11]
                    elif pack[i + 1] == 0x02:
                        self.data_dict[key]["number"] = {
                            "data": [pack[i + 3], pack[i + 4], pack[i + 5], pack[i + 6]],
                            "value": (pack[i + 3] >> 3) + (pack[i + 4] >> 2) + (pack[i + 5] >> 1) + pack[i + 6]
                            }
                # elif pack[i + 6] == 0xC1:
                #     is_c1_last = False
        except Exception as exc:
            print(f"{exc}")

        self.save()

    def parse_head(self, pack, key):
        """ Documentation for a method parse_head. Added: 30.09.2021 08:59 volodymyr.tyshchenko

        :param pack:
        :type pack:
        :param key:
        :type key:

        :return element index in data
        :rtype int
        """
        self.data_dict[key]["Length"] = pack[2]

        self.data_dict[key]["addr_from"], i = self.get_addr(idx=3, data=pack)
        self.data_dict[key]["addr_to"], i = self.get_addr(idx=i, data=pack)
        self.data_dict[key]["next"] = pack[i]

        self.data_dict[key]["in_out"] = {"value": pack[10], "direction": "out" if pack[10] == 0xE6 else "in"}
        self.data_dict[key]["pack_type"] = pack[i + 6]

        return i + 6
