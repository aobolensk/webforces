# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI/UI/SignupWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(846, 683)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.authenticationField = QtWidgets.QGroupBox(self.centralwidget)
        self.authenticationField.setGeometry(QtCore.QRect(160, 80, 431, 421))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.authenticationField.sizePolicy().hasHeightForWidth())
        self.authenticationField.setSizePolicy(sizePolicy)
        self.authenticationField.setTitle("")
        self.authenticationField.setAlignment(QtCore.Qt.AlignCenter)
        self.authenticationField.setObjectName("authenticationField")
        self.label = QtWidgets.QLabel(self.authenticationField)
        self.label.setGeometry(QtCore.QRect(40, 20, 141, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.AutoText)
        self.label.setObjectName("label")
        self.usernameEdit = QtWidgets.QLineEdit(self.authenticationField)
        self.usernameEdit.setGeometry(QtCore.QRect(40, 50, 350, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.usernameEdit.sizePolicy().hasHeightForWidth())
        self.usernameEdit.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(20)
        self.usernameEdit.setFont(font)
        self.usernameEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.usernameEdit.setText("")
        self.usernameEdit.setAlignment(QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.usernameEdit.setObjectName("usernameEdit")
        self.label_2 = QtWidgets.QLabel(self.authenticationField)
        self.label_2.setGeometry(QtCore.QRect(40, 120, 120, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.passwordEdit = QtWidgets.QLineEdit(self.authenticationField)
        self.passwordEdit.setGeometry(QtCore.QRect(40, 150, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(20)
        self.passwordEdit.setFont(font)
        self.passwordEdit.setObjectName("passwordEdit")
        self.pushButton = QtWidgets.QPushButton(self.authenticationField)
        self.pushButton.setGeometry(QtCore.QRect(40, 350, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.passwordConfimationEdit = QtWidgets.QLineEdit(self.authenticationField)
        self.passwordConfimationEdit.setGeometry(QtCore.QRect(40, 260, 350, 40))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(20)
        self.passwordConfimationEdit.setFont(font)
        self.passwordConfimationEdit.setObjectName("passwordConfimationEdit")
        self.label_3 = QtWidgets.QLabel(self.authenticationField)
        self.label_3.setGeometry(QtCore.QRect(40, 220, 351, 30))
        font = QtGui.QFont()
        font.setFamily("Calibri Light")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.errorMessage = QtWidgets.QLabel(self.authenticationField)
        self.errorMessage.setGeometry(QtCore.QRect(80, 300, 281, 30))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.errorMessage.setFont(font)
        self.errorMessage.setText("")
        self.errorMessage.setObjectName("errorMessage")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 846, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Username"))
        self.label_2.setText(_translate("MainWindow", "Password"))
        self.pushButton.setText(_translate("MainWindow", "Sign up for WebForces"))
        self.label_3.setText(_translate("MainWindow", "Password confirmation"))
