import pytest
from selenium import webdriver
from api.kinopoisk_api import KinopoiskAPI


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--incognito")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    driver.implicitly_wait(30)
    yield driver
    driver.quit()


@pytest.fixture
def api_client():
    return KinopoiskAPI()


def pytest_configure(config):
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "ui: UI tests")
