#!/usr/bin/env python3
import sys

from PyQt5.QtWidgets import QApplication

from GUI.Py import ui


def main():
    app = QApplication(sys.argv)
    loginWin = ui.LoginWindow()
    loginWin.show()
    app.exec_()
    return 0


if __name__ == '__main__':
    rc = main()
    sys.exit(rc)
