import time
from selenium.webdriver.remote.webdriver import WebDriver


def sign_in_user(selenium: WebDriver):
    selenium.find_element_by_id("SignInButton").click()
    selenium.find_element_by_name("username").send_keys("chifir")
    selenium.find_element_by_name("password").send_keys("thispasswordistooshort")
    selenium.find_element_by_id("SubmitLoginButton").click()


def sign_in_superuser(selenium: WebDriver):
    selenium.find_element_by_id("SignInButton").click()
    selenium.find_element_by_name("username").send_keys("walrus")
    selenium.find_element_by_name("password").send_keys("wal")
    selenium.find_element_by_id("SubmitLoginButton").click()


def add_new_alg(selenium: WebDriver):
    alg_title = "test_alg" + str(time.time()) + "|" + str(time.monotonic())
    selenium.find_element_by_id("NewAlgTitle").send_keys(alg_title)
    selenium.find_element_by_id("id_language_0").click()
    selenium.find_element_by_id("NewAlgDescription").send_keys("walp")
    selenium.find_element_by_id("NewAlgCost").send_keys("600")
    selenium.find_element_by_id("NewAlgSource").send_keys(
        "#include <iostream>\nint main(){std::cout << \"wal\" << std::endl;}")
    selenium.find_element_by_xpath("//button[@type='submit']").click()
    selenium.switch_to.alert.accept()
    return alg_title
