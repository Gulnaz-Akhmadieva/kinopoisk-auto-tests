from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MainPage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 30)
        self.url = "https://www.kinopoisk.ru"

    def open(self) -> "MainPage":
        self.driver.get(self.url)
        self.wait.until(EC.presence_of_element_located((By.NAME, "kp_query")))
        return self

    def search_by_year(self, year: str) -> None:
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.clear()
        search_input.send_keys(year)

    def search(self, query: str, film_id: str) -> None:
        search_input = self.driver.find_element(By.NAME, "kp_query")
        search_input.clear()
        search_input.send_keys(query)

        element = self.wait.until(EC.presence_of_element_located((By.ID, f"suggest-item-film-{film_id}")))
        self.driver.execute_script("arguments[0].click();", element)
        self.wait.until(lambda d: "film" in d.current_url)
