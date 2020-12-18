import pytest
from selenium.webdriver.remote.webdriver import WebDriver

@pytest.mark.web_test
def test_can_get_start_page(selenium: WebDriver):
    selenium.get("http://127.0.0.1:8000/")
