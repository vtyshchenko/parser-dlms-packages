import sys

from PyQt5.QtWidgets import QApplication

from view.main_view import MainView
# from view.conf_com_devices_view import CommDevConfView


if __name__ == "__main__":
    __version__ = "0.0.1"
    app = QApplication(sys.argv)

    try:
        window = MainView(user_name=user)
        window.show()
        sys.exit(app.exec_())
    except Exception as exc:
        print(exc)
