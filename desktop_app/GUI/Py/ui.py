from PyQt5 import QtWidgets

import LoginWindow
import MainWindow


def checkAuth(login, password):
    return 1 if login == "Anton" and password == "Molodec" else 0


class LoginWindow(QtWidgets.QMainWindow, LoginWindow.Ui_LoginWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.logBtn)

    def logBtn(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()
        if checkAuth(login, password):
            self.mainWin = MainWindow()
            self.mainWin.show()
            self.close()
        else:
            self.incorrectData.setText("Invalid login or password")


class MainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.storeButton.clicked.connect(self.storeBtn)
        self.profileButton.clicked.connect(self.profileBtn)
        self.statisticButton.clicked.connect(self.statisticBtn)
        self.outButton.clicked.connect(self.outBtn)

    def storeBtn(self):
        print("storeBtn")

    def profileBtn(self):
        print("profileBtn")

    def statisticBtn(self):
        print("statisticBtn")

    def outBtn(self):
        self.loginWin = LoginWindow()
        self.loginWin.show()
        self.close()
