import time
import pytest
from selenium.webdriver.remote.webdriver import WebDriver
from webforces.server import selenium_traits


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


@pytest.mark.web_test
def test_can_add_algorithm(selenium: WebDriver):
    selenium.get(base_url)
    selenium_traits.sign_in_user(selenium)

    selenium.find_element_by_id("StoreButton").click()
    selenium.find_element_by_id("AddNewAlgorithmButton").click()

    alg_title = "test_alg" + str(time.time()) + "|" + str(time.monotonic())
    selenium.find_element_by_id("NewAlgTitle").send_keys(alg_title)
    selenium.find_element_by_id("id_language_0").click()
    selenium.find_element_by_id("NewAlgDescription").send_keys("walp")
    selenium.find_element_by_id("NewAlgCost").send_keys("600")
    selenium.find_element_by_id("NewAlgSource").send_keys(
        "#include <iostream>\nint main(){std::cout << \"wal\" << std::endl;}")
    selenium.find_element_by_xpath("//button[@type='submit']").click()

    selenium.switch_to.alert.accept()
    selenium.find_element_by_xpath("//h2[text()='" + alg_title + "']")


@pytest.mark.web_test
def test_can_add_test_to_algorithm(selenium: WebDriver):
    selenium.get(base_url)
    selenium_traits.sign_in_user(selenium)

    selenium.find_element_by_id("StoreButton").click()
    selenium.find_element_by_id("AddNewAlgorithmButton").click()
    alg_title = selenium_traits.add_new_alg(selenium)

    elem = selenium.find_element_by_xpath("//h2[text()='" + alg_title + "']")
    elem.find_element_by_xpath("../a").click()

    selenium.find_element_by_id("AddTestButton").click()
    selenium.find_element_by_id("Title").send_keys("test1")
    selenium.find_element_by_id("NewTestInput").send_keys("wal")
    selenium.find_element_by_id("NewTestOutput").send_keys("wal")
    selenium.find_element_by_xpath("//button[@type='submit']").click()

    selenium.switch_to.alert.accept()
    selenium.find_element_by_xpath("//h2[text()='Found 1 tests']")


@pytest.mark.web_test
def test_can_run_validation(selenium: WebDriver):
    selenium.get(base_url)
    selenium_traits.sign_in_user(selenium)

    selenium.find_element_by_id("StoreButton").click()
    selenium.find_element_by_id("AddNewAlgorithmButton").click()
    alg_title = selenium_traits.add_new_alg(selenium)

    elem = selenium.find_element_by_xpath("//h2[text()='" + alg_title + "']")
    elem.find_element_by_xpath("../a").click()

    selenium.find_element_by_id("AddTestButton").click()
    selenium.find_element_by_id("Title").send_keys("test1")
    selenium.find_element_by_id("NewTestInput").send_keys("wal")
    selenium.find_element_by_id("NewTestOutput").send_keys("wal")
    selenium.find_element_by_xpath("//button[@type='submit']").click()
    selenium.switch_to.alert.accept()

    selenium.find_element_by_id("RunTestsButton").click()
