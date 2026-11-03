import allure
import requests

from constants import (
    BASE_URL,
    INGREDIENTS_ENDPOINT,
    LOGIN_ENDPOINT,
    ORDERS_ENDPOINT,
    REGISTER_ENDPOINT,
    USER_ENDPOINT,
)


class ApiClient:
    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {"Content-Type": "application/json"}

    def set_token(self, token):
        self.headers["Authorization"] = token

    @allure.step("Регистрация пользователя: {email}")
    def register_user(self, email, password, name):
        payload = {"email": email, "password": password, "name": name}
        return requests.post(f"{self.base_url}{REGISTER_ENDPOINT}", json=payload)

    @allure.step("Авторизация пользователя: {email}")
    def login_user(self, email, password):
        payload = {"email": email, "password": password}
        return requests.post(f"{self.base_url}{LOGIN_ENDPOINT}", json=payload)

    @allure.step("Изменение данных пользователя")
    def update_user(self, payload):
        return requests.patch(
            f"{self.base_url}{USER_ENDPOINT}",
            json=payload,
            headers=self.headers,
        )

    @allure.step("Удаление пользователя")
    def delete_user(self):
        return requests.delete(
            f"{self.base_url}{USER_ENDPOINT}",
            headers=self.headers,
        )

    @allure.step("Создание заказа")
    def create_order(self, ingredients):
        return requests.post(
            f"{self.base_url}{ORDERS_ENDPOINT}",
            json={"ingredients": ingredients},
            headers=self.headers,
        )

    @allure.step("Получение заказов пользователя")
    def get_user_orders(self):
        return requests.get(
            f"{self.base_url}{ORDERS_ENDPOINT}",
            headers=self.headers,
        )

    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        return requests.get(f"{self.base_url}{INGREDIENTS_ENDPOINT}")