import pytest

from utils.api_client import ApiClient
from utils.data_generator import generate_random_email, generate_random_string


@pytest.fixture
def api_client():
    """Базовый клиент без авторизации."""
    return ApiClient()


@pytest.fixture
def registered_user(api_client):
    """
    Создаёт уникального пользователя через API и удаляет его после теста.
    Возвращает словарь с данными пользователя и токеном.
    """
    email = generate_random_email()
    password = generate_random_string()
    name = generate_random_string()

    response = api_client.register_user(email, password, name)
    assert response.status_code == 200, (
        f"Не удалось создать пользователя в фикстуре: {response.text}"
    )
    data = response.json()
    token = data["accessToken"]

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


@pytest.fixture
def valid_ingredient_ids(api_client):
    """Возвращает список валидных ID ингредиентов для создания заказа."""
    response = api_client.get_ingredients()
    assert response.status_code == 200, "Не удалось получить список ингредиентов"
    return [item["_id"] for item in response.json()["data"][:2]]


@pytest.fixture
def cleanup_user():
    """
    Гарантированно удаляет созданных в тесте пользователей после его завершения.
    Работает даже если тест упал на assert.
    """
    tokens = []

    def add_token(token):
        tokens.append(token)

    yield add_token

    for token in tokens:
        client = ApiClient()
        client.set_token(token)
        client.delete_user()