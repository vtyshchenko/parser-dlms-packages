# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 595)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabs = QtWidgets.QTabWidget(self.centralwidget)
        self.tabs.setObjectName("tabs")
        self.tbOne = QtWidgets.QWidget()
        self.tbOne.setObjectName("tbOne")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.tbOne)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.splitter = QtWidgets.QSplitter(self.tbOne)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.layoutWidget_5 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.lblPackage = QtWidgets.QLabel(self.layoutWidget_5)
        self.lblPackage.setObjectName("lblPackage")
        self.verticalLayout_7.addWidget(self.lblPackage)
        self.plntxtedtPackage = QtWidgets.QPlainTextEdit(self.layoutWidget_5)
        self.plntxtedtPackage.setMinimumSize(QtCore.QSize(500, 150))
        self.plntxtedtPackage.setObjectName("plntxtedtPackage")
        self.verticalLayout_7.addWidget(self.plntxtedtPackage)
        self.trwdtResult = QtWidgets.QTreeWidget(self.splitter)
        self.trwdtResult.setMinimumSize(QtCore.QSize(0, 300))
        self.trwdtResult.setAlternatingRowColors(True)
        self.trwdtResult.setColumnCount(2)
        self.trwdtResult.setObjectName("trwdtResult")
        self.trwdtResult.headerItem().setText(0, "Ключ")
        self.trwdtResult.headerItem().setTextAlignment(0, QtCore.Qt.AlignCenter)
        self.trwdtResult.headerItem().setText(1, "Значення")
        self.trwdtResult.headerItem().setTextAlignment(1, QtCore.Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.splitter)
        self.tabs.addTab(self.tbOne, "")
        self.tbMany = QtWidgets.QWidget()
        self.tbMany.setObjectName("tbMany")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.tbMany)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.splitter_2 = QtWidgets.QSplitter(self.tbMany)
        self.splitter_2.setOrientation(QtCore.Qt.Vertical)
        self.splitter_2.setObjectName("splitter_2")
        self.layoutWidget_3 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.lblPackages = QtWidgets.QLabel(self.layoutWidget_3)
        self.lblPackages.setObjectName("lblPackages")
        self.verticalLayout_4.addWidget(self.lblPackages)
        self.txtedtPackages = QtWidgets.QTextEdit(self.layoutWidget_3)
        self.txtedtPackages.setObjectName("txtedtPackages")
        self.verticalLayout_4.addWidget(self.txtedtPackages)
        self.layoutWidget_4 = QtWidgets.QWidget(self.splitter_2)
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.lblResult = QtWidgets.QLabel(self.layoutWidget_4)
        self.lblResult.setObjectName("lblResult")
        self.verticalLayout_5.addWidget(self.lblResult)
        self.txtedtResult = QtWidgets.QTextEdit(self.layoutWidget_4)
        self.txtedtResult.setReadOnly(True)
        self.txtedtResult.setMarkdown("")
        self.txtedtResult.setObjectName("txtedtResult")
        self.verticalLayout_5.addWidget(self.txtedtResult)
        self.verticalLayout_6.addWidget(self.splitter_2)
        self.prgrsbrPackagesParse = QtWidgets.QProgressBar(self.tbMany)
        self.prgrsbrPackagesParse.setMinimumSize(QtCore.QSize(0, 0))
        self.prgrsbrPackagesParse.setMaximumSize(QtCore.QSize(16777215, 10))
        self.prgrsbrPackagesParse.setProperty("value", 24)
        self.prgrsbrPackagesParse.setObjectName("prgrsbrPackagesParse")
        self.verticalLayout_6.addWidget(self.prgrsbrPackagesParse)
        self.tabs.addTab(self.tbMany, "")
        self.verticalLayout.addWidget(self.tabs)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuOperation = QtWidgets.QMenu(self.menubar)
        self.menuOperation.setObjectName("menuOperation")
        self.menuHelp = QtWidgets.QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.tlbrOperations = QtWidgets.QToolBar(MainWindow)
        self.tlbrOperations.setObjectName("tlbrOperations")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.tlbrOperations)
        self.actionExit = QtWidgets.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("ico/exit.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        self.actionLoad = QtWidgets.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("ico/open.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad.setIcon(icon1)
        self.actionLoad.setObjectName("actionLoad")
        self.actionAnalize = QtWidgets.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("ico/analyze.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAnalize.setIcon(icon2)
        self.actionAnalize.setObjectName("actionAnalize")
        self.actionCopy = QtWidgets.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("ico/clipboard.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionCopy.setIcon(icon3)
        self.actionCopy.setObjectName("actionCopy")
        self.actionSave = QtWidgets.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("ico/save.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave.setIcon(icon4)
        self.actionSave.setObjectName("actionSave")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("ico/help.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionHelp.setIcon(icon5)
        self.actionHelp.setObjectName("actionHelp")
        self.actionAbout = QtWidgets.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("ico/about.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon6)
        self.actionAbout.setObjectName("actionAbout")
        self.menuFile.addAction(self.actionLoad)
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionExit)
        self.menuOperation.addAction(self.actionAnalize)
        self.menuOperation.addAction(self.actionCopy)
        self.menuHelp.addAction(self.actionHelp)
        self.menuHelp.addAction(self.actionAbout)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuOperation.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        self.tabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.lblPackage.setText(_translate("MainWindow", "Package"))
        self.tabs.setTabText(self.tabs.indexOf(self.tbOne), _translate("MainWindow", "One"))
        self.lblPackages.setText(_translate("MainWindow", "Packages"))
        self.lblResult.setText(_translate("MainWindow", "Result"))
        self.txtedtResult.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'MS Shell Dlg 2\';\"><br /></p></body></html>"))
        self.tabs.setTabText(self.tabs.indexOf(self.tbMany), _translate("MainWindow", "Many"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuOperation.setTitle(_translate("MainWindow", "Operation"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.tlbrOperations.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setShortcut(_translate("MainWindow", "Ctrl+X"))
        self.actionLoad.setText(_translate("MainWindow", "Load"))
        self.actionLoad.setToolTip(_translate("MainWindow", "Load file"))
        self.actionLoad.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionAnalize.setText(_translate("MainWindow", "Analyze"))
        self.actionAnalize.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.actionCopy.setText(_translate("MainWindow", "Copy"))
        self.actionCopy.setToolTip(_translate("MainWindow", "Copy to clipboard result"))
        self.actionCopy.setShortcut(_translate("MainWindow", "Ctrl+C"))
        self.actionSave.setText(_translate("MainWindow", "Save"))
        self.actionSave.setToolTip(_translate("MainWindow", "Save to file result"))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))
        self.actionHelp.setShortcut(_translate("MainWindow", "F1"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAbout.setShortcut(_translate("MainWindow", "Shift+F1"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
