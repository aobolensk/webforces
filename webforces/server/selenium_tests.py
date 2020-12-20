import pytest
from selenium.webdriver.remote.webdriver import WebDriver


base_url: str = "http://127.0.0.1:8000/"


@pytest.fixture
def firefox_options(firefox_options):
    firefox_options.add_argument("--headless")
    return firefox_options


@pytest.mark.web_test
def test_can_autentificate_user(selenium: WebDriver):
    selenium.get(base_url)
    sign_in_elem = selenium.find_element_by_id("SignInButton")
    sign_in_elem.click()

    username_elem = selenium.find_element_by_name("username")
    username_elem.send_keys("chifir")
    password_elem = selenium.find_element_by_name("password")
    password_elem.send_keys("thispasswordistooshort")
    submit_elem = selenium.find_element_by_id("SubmitLoginButton")
    submit_elem.click()

    assert selenium.current_url == base_url


@pytest.mark.web_test
def test_cant_autentificate_wrong_user(selenium: WebDriver):
    selenium.get(base_url)
    sign_in_elem = selenium.find_element_by_id("SignInButton")
    sign_in_elem.click()

    username_elem = selenium.find_element_by_name("username")
    username_elem.send_keys("chifir")
    password_elem = selenium.find_element_by_name("password")
    password_elem.send_keys("chifir")
    submit_elem = selenium.find_element_by_id("SubmitLoginButton")
    submit_elem.click()
    error_elem = selenium.find_element_by_name("MessageParagraph")

    assert error_elem.text == "Incorrect username or password"


@pytest.mark.web_test
def test_cant_registrate_with_empty_fields(selenium: WebDriver):
    selenium.get(base_url)
    selenium.find_element_by_id("SignUpButton").click()

    selenium.find_element_by_id("SubmitSignUpButton").click()

    assert selenium.current_url == base_url + "accounts/sign_up/"


@pytest.mark.web_test
def test_can_sign_out(selenium: WebDriver):
    selenium.get(base_url)
    selenium.find_element_by_id("SignInButton").click()
    selenium.find_element_by_name("username").send_keys("chifir")
    selenium.find_element_by_name("password").send_keys("thispasswordistooshort")
    selenium.find_element_by_id("SubmitLoginButton").click()

    selenium.find_element_by_id("SignOutButton").click()

    assert selenium.current_url == base_url
    selenium.find_element_by_id("SignInButton")


@pytest.mark.web_test
def test_can_access_password_reset_page(selenium: WebDriver):
    selenium.get(base_url)
    selenium.find_element_by_id("SignInButton").click()

    selenium.find_element_by_id("ForgotPasswordLink").click()

    assert selenium.current_url == base_url + "accounts/password_reset/"


@pytest.mark.web_test
def test_can_navigate_to_store(selenium: WebDriver):
    selenium.get(base_url)
    selenium.find_element_by_id("SignInButton").click()
    selenium.find_element_by_name("username").send_keys("chifir")
    selenium.find_element_by_name("password").send_keys("thispasswordistooshort")
    selenium.find_element_by_id("SubmitLoginButton").click()

    selenium.find_element_by_id("StoreButton").click()

    assert selenium.current_url == base_url + "store/"


@pytest.mark.web_test
def test_can_navigate_to_user_profile(selenium: WebDriver):
    selenium.get(base_url)
    selenium.find_element_by_id("SignInButton").click()
    selenium.find_element_by_name("username").send_keys("chifir")
    selenium.find_element_by_name("password").send_keys("thispasswordistooshort")
    selenium.find_element_by_id("SubmitLoginButton").click()

    selenium.find_element_by_id("UserProfileButton").click()

    assert selenium.current_url == base_url + "users/chifir/"


@pytest.mark.web_test
def test_can_see_statistic_by_superuser(selenium: WebDriver):
    selenium.get(base_url)
    selenium.find_element_by_id("SignInButton").click()
    selenium.find_element_by_name("username").send_keys("walrus")
    selenium.find_element_by_name("password").send_keys("wal")
    selenium.find_element_by_id("SubmitLoginButton").click()

    selenium.find_element_by_id("StatisticsButton").click()

    assert selenium.current_url == base_url + "stats/"
