from PyQt5 import QtWidgets

import requests
import LoginWindow
import MainWindow
import SignupWindow


class LoginWindow(QtWidgets.QMainWindow, LoginWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.logBtn)

    def resizeEvent(self, event):
        self.authenticationField.move(self.centralwidget.width()/2 - self.authenticationField.width()/2,
                                      self.centralwidget.height()/2 - self.authenticationField.height()/2)

    def logBtn(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()
        if self.checkAuth(login, password):
            self.mainWin = MainWindow(self.token)
            self.mainWin.show()
            self.close()
        else:
            self.incorrectData.setText("Invalid login or password")

    def checkAuth(self, login, password):
        response = requests.post('http://127.0.0.1:8000/api/get_token/',
                                 data={'username': login, 'password': password})
        if response.status_code != 200:
            return 0
        self.token = response.json()['auth_token']
        return 1

    def signUpBtn(self):
        self.signUpWin = SignupWindow()
        self.signUpWin.show()
        self.close()


class SignupWindow(QtWidgets.QMainWindow, SignupWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.SignUpBtn)

    def resizeEvent(self, event):
        self.authenticationField.move(self.centralwidget.width()/2 - self.authenticationField.width()/2,
                                      self.centralwidget.height()/2 - self.authenticationField.height()/2)

    def SignUpBtn(self):
        username = self.usernameEdit.text()
        password = self.passwordEdit.text()
        password_confimation = self.passwordConfimationEdit.text()
        if self.checkUsername(username) and self.checkPassword(password, password_confimation):
            self.loginWin = LoginWindow()
            self.loginWin.show()
            self.close()
        else:
            self.errorMessage.setText("Invalid username or password")

    def checkPassword(self, password, password_confimation):
        return 1

    def checkUsername(self, username):
        return 1


class MainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, token):
        super().__init__()
        self.token = token
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
        response = requests.get('http://127.0.0.1:8000/api/stats/', headers={'Authorization': 'Token ' + self.token})
        if response.status_code == 200:
            statistics = response.json()
            for key, value in statistics.items():
                self.results.setText(self.results.text() + key + " : " + value + '\n')

    def outBtn(self):
        self.loginWin = LoginWindow()
        self.loginWin.show()
        self.close()
