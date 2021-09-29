"""
Added: 13.09.2018 16:31    volodymyr.tyshchenko

module for works with json file
"""
import json

from os.path import isfile
from PyQt5.QtWidgets import QMessageBox


class Json:
    """
    Json
    """
    def __init__(self):
        self.error = None

    def load_file(self, file_name):
        """ Documentation for a method load_file.  Added: 13.09.2018 16:31
        load json file into dict

        :param file_name: file path and file name for load data

        :return: data in dictionary from json file
        :rtype: dict
        """
        if isfile(file_name):
            self.error = None
            try:
                with open(file_name, 'r') as file:
                    load_file = json.load(file)
                return load_file
            except Exception as exc:
                err = f"Error load file {file_name}: {exc}"
                self.error = err
                raise Exception(err)
        else:
            return None

    @staticmethod
    def save_file(file_name, p_out):
        """ Documentation for a method.  Added: 13.09.2018 16:33
         Save dict into json file

        :param file_name: json file path and name
        :type file_name: string
        :param p_out: data for save data in the file
        :type p_out: dict
        """
        try:
            with open(file_name, 'w') as file:
                json.dump(p_out, file, indent=4)
        except Exception as exc:
            err = f"Error saving file {file_name}: {exc}"
            raise Exception(err)

    def save_file_ex(self, file_name, p_out, ensure_ascii=True, is_file_exists=True):
        """ Documentation for a method save_json.  Added: 13.09.2018 16:33
         Save dict into json file

        :raise: Error saving file

        :param file_name: json file path and name
        :type file_name: string
        :param p_out: data for save data in the file
        :type p_out: dict
        :param ensure_ascii: If it is false, then the strings written to file can contain non-ASCII characters if they
        appear in strings contained in ``obj``. Otherwise, all such characters are escaped in JSON strings.
        :type ensure_ascii: bool
        :param is_file_exists: If it is true, then show message if file exists.
        :type is_file_exists: bool
         """
        res = True
        if isfile(file_name) and is_file_exists:
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("File exists!")
            s = f"File {file_name} exists. Overwrite?"
            msg_box.setText(s)
            msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg_box.setDefaultButton(QMessageBox.No)
            resp = msg_box.exec_()
            if resp == QMessageBox.No:
                s = f"Template is not saved!"
                msg_box.setText(s)
                msg_box.setStandardButtons(QMessageBox.Ok | QMessageBox.Ok)
                msg_box.setDefaultButton(QMessageBox.Ok)
                msg_box.exec_()
                res = False
        if res:
            self.error = None
            try:
                with open(file_name, 'w') as file:
                    json.dump(p_out, file, indent=4, ensure_ascii=ensure_ascii)
            except Exception as exc:
                err = f"Error saving file {file_name}: {exc}"
                self.error = err
                raise Exception(err)

    @staticmethod
    def dumps(data):
        """Documentation for a method dumps.  Added:
        Save dictionary into json file.

        :param data: :type file descriptor: point to file

        :return: dictionary
        :rtype: dict
        """
        return json.dumps(data)

    @staticmethod
    def loads(data):
        """Documentation for a method loads.  Added:
        load json file into dictionary.

        :param data: :type file descriptor: point to file

        :return: dictionary
        :rtype: dict
        """
        return json.loads(data)


if __name__ == "__main__":
    pass
