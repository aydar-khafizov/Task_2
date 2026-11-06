import allure
import pytest

from constants import ERROR_REQUIRED_FIELDS, ERROR_USER_EXISTS
from utils.data_generator import generate_random_email, generate_random_string


@allure.feature("Пользователи")
@allure.story("Создание пользователя")
class TestCreateUser:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, api_client, cleanup_user):
        email = generate_random_email()
        password = generate_random_string()
        name = generate_random_string()

        response = api_client.register_user(email, password, name)
        body = response.json()

        if "accessToken" in body:
            cleanup_user(body["accessToken"])

        assert response.status_code == 200
        assert body["success"] is True
        assert "accessToken" in body
        assert "refreshToken" in body
        assert body["user"]["email"] == email
        assert body["user"]["name"] == name

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user(self, api_client, registered_user):
        response = api_client.register_user(
            registered_user["email"],
            registered_user["password"],
            registered_user["name"],
        )

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_USER_EXISTS

    @allure.title("Создание пользователя без обязательного поля: {missing_field}")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_without_required_field(self, api_client, missing_field):
        payload = {
            "email": generate_random_email(),
            "password": generate_random_string(),
            "name": generate_random_string(),
        }
        payload.pop(missing_field)

        response = api_client.register_user(
            payload.get("email"),
            payload.get("password"),
            payload.get("name"),
        )

        assert response.status_code == 403
        body = response.json()
        assert body["success"] is False
        assert body["message"] == ERROR_REQUIRED_FIELDS