# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SceneWindow.ui'
#
# Created: Mon Sep  7 16:54:09 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_SceneWindow(object):
    def setupUi(self, SceneWindow):
        SceneWindow.setObjectName(_fromUtf8("SceneWindow"))
        SceneWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(SceneWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.graphicsView = Viewport(self.centralwidget)
        self.graphicsView.setMinimumSize(QtCore.QSize(0, 0))
        self.graphicsView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.graphicsView.setFrameShadow(QtGui.QFrame.Plain)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        SceneWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(SceneWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        SceneWindow.setStatusBar(self.statusbar)

        self.retranslateUi(SceneWindow)
        QtCore.QMetaObject.connectSlotsByName(SceneWindow)

    def retranslateUi(self, SceneWindow):
        SceneWindow.setWindowTitle(_translate("SceneWindow", "Cartwheel scene", None))

from Viewport import Viewport
