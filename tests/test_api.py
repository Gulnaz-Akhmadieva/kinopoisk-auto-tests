import allure
import pytest


# Тестовые данные для поиска
search_data = [
    ("Москва слезам не верит", 46708),
    ("Матрица", 301),
    ("Бриллиантовая рука", 46225)
]


@allure.title("Поиск фильма по названию")
@allure.feature("API")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.parametrize("query, expected_id", search_data)
def test_search_by_name(api_client, query, expected_id):
    """
    Позитивный тест поиска фильмов по названию.
    Проверяет, что для каждого названия находится фильм с ожидаемым ID.
    """
    with allure.step(f"Выполнить поиск по названию: {query}"):
        result = api_client.search_by_name(query)

    with allure.step("Проверить ответ сервера"):
        assert len(result["docs"]) > 0
        assert result["docs"][0]["name"] == query
        assert result["docs"][0]["id"] == expected_id


# Тестовые данные для поиска по ID
id_data = [
    (46708, "Москва слезам не верит"),
    (301, "Матрица"),
    (46225, "Бриллиантовая рука")
]


@allure.title("Поиск фильма по ID")
@allure.feature("API")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
@pytest.mark.parametrize("movie_id, expected_name", id_data)
def test_get_by_id(api_client, movie_id, expected_name):
    """
    Позитивный тест поиска фильмов по id.
    Проверяет, что при вводе id сервер возвращает информацию
    именно об этом фильме.
    """
    with allure.step(f"Получить фильм по ID: {movie_id}"):
        result = api_client.get_by_id(movie_id)

    with allure.step("Проверить ответ сервера"):
        assert result["id"] == movie_id
        assert result["name"] == expected_name


@allure.title("Получение информации о коллекции ТОП-250")
@allure.feature("API")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.api
def test_get_top250(api_client):
    """
    Позитивный тест, проверка получения информации о коллекции
    "ТОП-250 лучших фильмов".
    """
    with allure.step("Получить информацию о коллекции ТОП-250"):
        result = api_client.get_top250()

    with allure.step("Проверить данные коллекции"):
        assert result["slug"] == "top250"
        assert result["moviesCount"] == 250
        assert result["name"] == "250 лучших фильмов"


@allure.title("Запрос с неверным ID")
@allure.feature("API")
@allure.severity(allure.severity_level.MINOR)
@pytest.mark.api
def test_get_by_wrong_id(api_client):
    """
    Негативный тест, проверяем, что в поиске фильма при некорректном id
    сервер возвращает ошибку о значении поля id".
    """
    with allure.step("Выполнить запрос с неверным ID (999999999)"):
        result = api_client.get_by_id(999999999)

    with allure.step("Проверить сообщение об ошибке"):
        assert result["statusCode"] == 400
        assert "диапазоне от 250 до 15000000" in str(result["message"])


@allure.title("Запрос без токена")
@allure.feature("API")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.api
def test_get_by_id_no_key(api_client):
    """
    Негативный тест, проверяет, что сервер возвращает ошибку о
    том, что токен не указан".
    """
    with allure.step("Выполнить запрос без API-ключа"):
        result = api_client.get_by_id_no_key(46708)

    with allure.step("Проверить ошибку авторизации"):
        assert result["statusCode"] == 401
        assert result["message"] == "В запросе не указан токен!"
