import allure

from constants import ERROR_INCORRECT_CREDENTIALS
from utils.data_generator import generate_random_email, generate_random_string


@allure.feature("Пользователи")
@allure.story("Логин")
class TestLogin:

    @allure.title("Логин под существующим пользователем")
    def test_login_valid_credentials(self, api_client, registered_user):
        response = api_client.login_user(
            registered_user["email"],
            registered_user["password"],
        )

        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == registered_user["email"]

    @allure.title("Логин с неверным email")
    def test_login_invalid_email(self, api_client, registered_user):
        response = api_client.login_user(
            generate_random_email(),
            registered_user["password"],
        )

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_INCORRECT_CREDENTIALS

    @allure.title("Логин с неверным паролем")
    def test_login_invalid_password(self, api_client, registered_user):
        response = api_client.login_user(
            registered_user["email"],
            generate_random_string(),
        )

        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_INCORRECT_CREDENTIALS