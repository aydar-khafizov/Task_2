import pytest

from utils.api_client import ApiClient
from utils.data_generator import generate_random_email, generate_random_string


@pytest.fixture
def api_client():
    """Базовый клиент без авторизации."""
    return ApiClient()


@pytest.fixture
def registered_user():
    """
    Создаёт уникального пользователя и удаляет его после теста.
    Возвращает словарь с данными пользователя и токеном.
    """
    client = ApiClient()
    email = generate_random_email()
    password = generate_random_string()
    name = generate_random_string()

    response = client.register_user(email, password, name)
    assert response.status_code == 200, (
        f"Не удалось создать пользователя в фикстуре: {response.text}"
    )
    token = response.json()["accessToken"]

    yield {
        "email": email,
        "password": password,
        "name": name,
        "token": token,
    }

    # Cleanup: удаление пользователя после теста
    cleanup_client = ApiClient()
    cleanup_client.set_token(token)
    cleanup_client.delete_user()


@pytest.fixture
def authorized_client(registered_user):
    """Клиент с авторизацией созданного пользователя."""
    client = ApiClient()
    client.set_token(registered_user["token"])
    return client