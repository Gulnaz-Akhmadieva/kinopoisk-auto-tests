import requests
from config import BASE_URL, API_KEY


class KinopoiskAPI:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            "X-API-KEY": API_KEY,
            "Content-Type": "application/json"
        }

    def search_by_name(self, query: str, limit: int = 10) -> dict:
        """Поиск фильма по названию."""
        url = f"{self.base_url}/movie/search"
        params = {"page": 1, "limit": limit, "query": query}
        response = requests.get(url, headers=self.headers, params=params)
        return response.json()

    def get_by_id(self, movie_id: int) -> dict:
        """Поиск фильма по ID."""
        url = f"{self.base_url}/movie/{movie_id}"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_top250(self) -> dict:
        """Получение топ-250 фильмов."""
        url = f"{self.base_url}/list/top250"
        response = requests.get(url, headers=self.headers)
        return response.json()

    def get_by_id_no_key(self, movie_id: int) -> dict:
        """Получение фильма по ID без API-ключа."""
        url = f"{self.base_url}/movie/{movie_id}"
        response = requests.get(url)
        return response.json()
