import allure

from constants import ERROR_UNAUTHORIZED
from utils.data_generator import generate_random_email, generate_random_string


@allure.feature("Пользователи")
@allure.story("Изменение данных пользователя")
class TestUpdateUser:

    @allure.title("Изменение email с авторизацией")
    def test_update_email_with_auth(self, authorized_client):
        new_email = generate_random_email()

        response = authorized_client.update_user({"email": new_email})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["email"] == new_email

    @allure.title("Изменение пароля с авторизацией")
    def test_update_password_with_auth(
        self, api_client, authorized_client, registered_user
    ):
        new_password = generate_random_string()

        response = authorized_client.update_user({"password": new_password})

        assert response.status_code == 200
        assert response.json()["success"] is True

        # Проверяем, что с новым паролем можно войти
        login_response = api_client.login_user(
            registered_user["email"], new_password
        )
        assert login_response.status_code == 200
        assert login_response.json()["success"] is True

    @allure.title("Изменение имени с авторизацией")
    def test_update_name_with_auth(self, authorized_client):
        new_name = generate_random_string()

        response = authorized_client.update_user({"name": new_name})

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["user"]["name"] == new_name

    @allure.title("Изменение данных без авторизации")
    def test_update_user_without_auth(self, api_client):
        response = api_client.update_user({"email": generate_random_email()})

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_UNAUTHORIZED