import allure

from constants import ERROR_UNAUTHORIZED


@allure.feature("Заказы")
@allure.story("Получение заказов пользователя")
class TestGetOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_orders_with_auth(self, authorized_client):
        response = authorized_client.get_user_orders()

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "orders" in body
        assert isinstance(body["orders"], list)
        assert "total" in body
        assert "totalToday" in body

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_orders_without_auth(self, api_client):
        response = api_client.get_user_orders()

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_UNAUTHORIZED