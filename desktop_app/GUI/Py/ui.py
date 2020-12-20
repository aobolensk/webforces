from PyQt5 import QtWidgets

import requests
from GUI.Py import LoginWindow
from GUI.Py import MainWindow
from GUI.Py import SignupWindow
from GUI.Py import Profile
from GUI.Py import Statistic


class LoginWindow(QtWidgets.QMainWindow, LoginWindow.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.pushButton.clicked.connect(self.logBtn)
        self.loginEdit.returnPressed.connect(self.logBtn)
        self.passwordEdit.returnPressed.connect(self.logBtn)

    def resizeEvent(self, event):
        self.authenticationField.move(self.centralwidget.width()//2 - self.authenticationField.width()//2,
                                      self.centralwidget.height()//2 - self.authenticationField.height()//2)

    def logBtn(self):
        login = self.loginEdit.text()
        password = self.passwordEdit.text()
        status = self.checkAuth(login, password)
        if status == 1:
            self.mainWin = MainWindow(self.token, login)
            self.mainWin.show()
            self.close()
        elif status == 0:
            self.incorrectData.setText("Invalid login or password")
        else:
            self.incorrectData.setText("Cannot connect to server")

    def checkAuth(self, login, password):
        try:
            response = requests.post('http://127.0.0.1:8000/api/get_token/',
                                     data={'username': login, 'password': password})

            if response.status_code != 200:
                return 0
            self.token = response.json()['auth_token']
            return 1
        except Exception:
            return 2

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
        self.authenticationField.move(self.centralwidget.width()//2 - self.authenticationField.width()//2,
                                      self.centralwidget.height()//2 - self.authenticationField.height()//2)

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


class statistic(QtWidgets.QGroupBox, Statistic.Ui_GroupBox):
    def __init__(self, parent, token):
        super().__init__(parent)
        self.setupUi(self)
        self.token = token
        self.getStats()

    def getStats(self):
        response = requests.get('http://127.0.0.1:8000/api/stats/', headers={'Authorization': 'Token ' + self.token})
        if response.status_code == 200:
            self.results.setText("")
            statistics = response.json()
            for key, value in statistics.items():
                self.results.setText(self.results.text() + str(key) + " : " + str(value) + '\n')


class profile(QtWidgets.QGroupBox, Profile.Ui_GroupBox):
    def __init__(self, parent, token, login):
        super().__init__(parent)
        self.setupUi(self)
        self.login = login
        self.token = token
        self.getUser()
        self.state = 1
        self.setDisabled()
        self.EditButton.clicked.connect(self.setDisabled)
        self.saveButton.clicked.connect(self.changeUser)

    def getUser(self):
        response = requests.get('http://127.0.0.1:8000/api/users/' + self.login,
                                headers={'Authorization': 'Token ' + self.token})
        if response.status_code == 200:
            profile = response.json()
            self.id = profile['id']
            self.UsernameEdit.setText(profile['login'])
            self.FirstNameEdit.setText(profile["first_name"])
            self.SecondNameEdit.setText(profile["second_name"])
            self.MiddleNameEdit.setText(profile["middle_name"])

    def changeUser(self):
        response = requests.post(
            'http://127.0.0.1:8000/api/users/' + self.login + '/',
            data={'first_name': self.FirstNameEdit.text(),
                  'second_name': self.SecondNameEdit.text(),
                  'middle_name': self.MiddleNameEdit.text()
                  },
            headers={'Authorization': 'Token ' + self.token}
        )
        status = ""
        if response.status_code == 200:
            status = response.json()
        return status

    def setDisabled(self):
        self.UsernameEdit.setReadOnly(True)
        self.FirstNameEdit.setReadOnly(self.state)
        self.SecondNameEdit.setReadOnly(self.state)
        self.MiddleNameEdit.setReadOnly(self.state)
        self.state = 1 - self.state


class MainWindow(QtWidgets.QMainWindow, MainWindow.Ui_MainWindow):
    def __init__(self, token, login):
        super().__init__()
        self.token = token
        self.login = login
        self.setupUi(self)
        self.InfoField.setVisible(False)
        self.storeButton.clicked.connect(self.storeBtn)
        self.profileButton.clicked.connect(self.profileBtn)
        self.statisticButton.clicked.connect(self.statisticBtn)
        self.outButton.clicked.connect(self.outBtn)

    def storeBtn(self):
        print("storeBtn")

    def profileBtn(self):
        self.InfoField.setVisible(False)
        self.InfoField = profile(self.ViewField, self.token, self.login)
        self.resizeEvent()
        self.InfoField.setVisible(True)

    def statisticBtn(self):
        self.InfoField.setVisible(False)
        self.InfoField = statistic(self.ViewField, self.token)
        self.resizeEvent()
        self.InfoField.setVisible(True)

    def resizeEvent(self, event=None):
        self.InfoField.move(self.ViewField.width()//2 - self.InfoField.width()//2,
                            self.ViewField.height()//2 - self.InfoField.height()//2)

    def outBtn(self):
        self.loginWin = LoginWindow()
        self.loginWin.show()
        self.close()
