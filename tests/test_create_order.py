import allure

from constants import ERROR_NO_INGREDIENTS


@allure.feature("Заказы")
@allure.story("Создание заказа")
class TestCreateOrder:

    @allure.title("Создание заказа с авторизацией и ингредиентами")
    def test_create_order_with_auth_and_ingredients(self, authorized_client, valid_ingredient_ids):
        response = authorized_client.create_order(valid_ingredient_ids)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body
        assert "number" in body["order"]

    @allure.title("Создание заказа с авторизацией без ингредиентов")
    def test_create_order_with_auth_without_ingredients(self, authorized_client):
        response = authorized_client.create_order([])

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_NO_INGREDIENTS

    @allure.title("Создание заказа с авторизацией и неверным хешем ингредиента")
    def test_create_order_with_auth_invalid_hash(self, authorized_client):
        response = authorized_client.create_order(["invalid_hash_123"])

        assert response.status_code == 500

    @allure.title("Создание заказа без авторизации с ингредиентами")
    def test_create_order_without_auth_with_ingredients(self, api_client, valid_ingredient_ids):
        response = api_client.create_order(valid_ingredient_ids)

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "order" in body

    @allure.title("Создание заказа без авторизации без ингредиентов")
    def test_create_order_without_auth_without_ingredients(self, api_client):
        response = api_client.create_order([])

        assert response.status_code == 400
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_NO_INGREDIENTS

    @allure.title("Создание заказа без авторизации с неверным хешем")
    def test_create_order_without_auth_invalid_hash(self, api_client):
        response = api_client.create_order(["invalid_hash_123"])

        assert response.status_code == 500