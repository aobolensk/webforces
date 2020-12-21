import pytest
from PyQt5.QtCore import Qt
from pytestqt.qtbot import QtBot
from desktop_app.GUI.Py import ui


@pytest.mark.app_test
def test_can_autentificate_user(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)

    qtbot.keyClicks(window.loginEdit, "chifir")
    qtbot.keyClicks(window.passwordEdit, "thispasswordistooshort")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)

    assert "mainWin" in window.__dict__
    assert window.mainWin is not None
    assert isinstance(window.mainWin, ui.MainWindow)


@pytest.mark.app_test
def test_cant_autentificate_user_with_wrong_login_or_password(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)

    qtbot.keyClicks(window.loginEdit, "chifir")
    qtbot.keyClicks(window.passwordEdit, "wal")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)

    assert window.incorrectData.text() == "Invalid login or password"
    assert "mainWin" not in window.__dict__


@pytest.mark.app_test
def test_can_reset_password(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)

    assert window.forgotPasswordLabel.text().find("Forgot password") != -1
    assert window.forgotPasswordLabel.text().find("http://localhost:8000/accounts/password_reset/") != -1
    assert window.forgotPasswordLabel.openExternalLinks()


@pytest.mark.app_test
def test_can_navigate_to_store(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)
    qtbot.keyClicks(window.loginEdit, "chifir")
    qtbot.keyClicks(window.passwordEdit, "thispasswordistooshort")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)
    main_window = window.mainWin

    qtbot.mouseClick(main_window.storeButton, Qt.LeftButton)

    assert main_window.InfoField.isVisible()
    assert isinstance(main_window.InfoField, ui.store)


@pytest.mark.app_test
def test_can_navigate_to_profile(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)
    qtbot.keyClicks(window.loginEdit, "chifir")
    qtbot.keyClicks(window.passwordEdit, "thispasswordistooshort")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)
    main_window = window.mainWin

    qtbot.mouseClick(main_window.profileButton, Qt.LeftButton)

    assert main_window.InfoField.isVisible()
    assert isinstance(main_window.InfoField, ui.profile)


@pytest.mark.app_test
def test_superuser_can_navigate_to_statistic(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)
    qtbot.keyClicks(window.loginEdit, "walrus")
    qtbot.keyClicks(window.passwordEdit, "wal")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)
    main_window = window.mainWin

    qtbot.mouseClick(main_window.statisticButton, Qt.LeftButton)

    assert main_window.InfoField.isVisible()
    assert isinstance(main_window.InfoField, ui.statistic)


@pytest.mark.skip(reason="statistic button exists")
@pytest.mark.app_test
def test_user_has_no_statistic_button(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)

    qtbot.keyClicks(window.loginEdit, "chifir")
    qtbot.keyClicks(window.passwordEdit, "thispasswordistooshort")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)

    assert "statisticButton" not in window.mainWin.__dict__


@pytest.mark.app_test
def test_can_sign_out(qtbot: QtBot):
    window = ui.LoginWindow()
    qtbot.addWidget(window)
    qtbot.keyClicks(window.loginEdit, "chifir")
    qtbot.keyClicks(window.passwordEdit, "thispasswordistooshort")
    qtbot.mouseClick(window.pushButton, Qt.LeftButton)
    main_window = window.mainWin

    qtbot.mouseClick(main_window.outButton, Qt.LeftButton)

    assert "loginWin" in main_window.__dict__
    assert main_window.loginWin is not None
    assert isinstance(main_window.loginWin, ui.LoginWindow)
