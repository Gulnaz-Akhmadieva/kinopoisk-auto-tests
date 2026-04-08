import allure
import pytest


@allure.title("Поиск фильма по названию")
@allure.feature("UI")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_search_by_name(driver):
    """
    Позитивный тест: поиск по названию фильма.
    """
    with allure.step("Открыть главную страницу и выполнить поиск"):
        from ui.pages.main_page import MainPage
        main_page = MainPage(driver)
        main_page.open()
        main_page.search("Москва слезам не верит", "46708")

    with allure.step("Проверить результат"):
        assert "46708" in driver.current_url


@allure.title("Поиск фильма по году")
@allure.feature("UI")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_search_by_year(driver):
    """
    Позитивный тест: поиск фильма при помощи года выпуска.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    with allure.step("Открыть главную страницу и ввести год"):
        driver.get("https://www.kinopoisk.ru")
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("1975")

    with allure.step("Выбрать фильм из выпадающего списка"):
        film = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.ID, "suggest-item-film-77301"))
        )
        film.click()

    with allure.step("Дождаться загрузки страницы фильма"):
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "[data-tid='75209b22']"))
        )


@allure.title("Поиск с лишними пробелами")
@allure.feature("UI")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_search_with_spaces(driver):
    """
    Позитивный тест: поиск с лишними пробелами в начале и в конце строки.
    """
    with allure.step("Открыть главную страницу и выполнить поиск"):
        from ui.pages.main_page import MainPage
        main_page = MainPage(driver)
        main_page.open()
        main_page.search("   Матрица   ", "301")

    with allure.step("Проверить результат"):
        assert "301" in driver.current_url


@allure.title("Поиск без запроса")
@allure.feature("UI")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.ui
def test_search_empty(driver):
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    """
    Негативный тест: поиск с пустым запросом.
    При клике на лупу с пустой строкой открывается
    страница с надписью "Случайный фильм".
    ВНИМАНИЕ: тест требует ручного прохождения капчи.
    При успешном прохождении капчи тест проходит автоматически.
    """
    with allure.step("Открыть главную страницу и нажать на лупу"):
        driver.get("https://www.kinopoisk.ru")
        search_button = driver.find_element(
            By.CSS_SELECTOR, ".search-form-submit-button__icon"
        )
        search_button.click()

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, ".randomMovieButton")
            )
        )


@allure.title("Поиск с недопустимыми символами")
@allure.feature("UI")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.ui
def test_search_invalid_chars(driver):
    """
    Негативный тест: в поисковую строку вводим спецсимволы.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    with allure.step("Открыть главную страницу и ввести спецсимволы"):
        driver.get("https://www.kinopoisk.ru")
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("!@#$%^&*()")
        search_input.submit()

    with allure.step("Проверить появление сообщения об ошибке"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//h2[@class="textorangebig" and contains(text(), '
                    '"К сожалению, по вашему запросу ничего не найдено")]')
            )
        )


@allure.title("Поиск фильма и проверка наличия рейтинга")
@allure.feature("UI")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.ui
def test_search_and_rating(driver):
    """
    Позитивный тест: поиск фильма и проверка наличия рейтинга.
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    with allure.step("Открыть главную страницу и ввести название фильма"):
        driver.get("https://www.kinopoisk.ru")
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("Бриллиантовая рука")

    with allure.step("Выбрать фильм из выпадающего списка"):
        film = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "suggest-item-film-46225"))
        )
        film.click()

    with allure.step("Проверить наличие рейтинга на странице фильма"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR,
                    ".styles_ratingValue__P9R1x.styles_rootMSize__S2PLT"))
        )


@allure.title("Поиск в неправильной раскладке")
@allure.feature("UI")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.ui
def test_search_wrong_layout(driver):
    """
    Негативный тест: поиск в английской раскладке, когда
    ожидается русское название.
    Проверяем, что в выпадающем списке появляется фильм 'Матрица' (ID 301).
    """
    from selenium.webdriver.common.by import By
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC

    with allure.step("Открыть главную страницу "
                     "и ввести запрос в английской раскладке"):
        driver.get("https://www.kinopoisk.ru")
        search_input = driver.find_element(By.NAME, "kp_query")
        search_input.send_keys("vanhbwf")  # "матрица" английскими буквами

    with allure.step("Проверить, что в выпадающем списке появилась 'Матрица'"):
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "suggest-item-film-301"))
        )
