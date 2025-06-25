import pytest
import requests
from helpers import generate_random_user
from config import BASE_URL

BASE_URL = "https://stellarburgers.nomoreparties.site/api"

@pytest.fixture
def random_user():
    """Генерирует случайного пользователя через функцию из helpers"""
    return generate_random_user()

@pytest.fixture
def registered_user(random_user):
    """Регистрирует пользователя, возвращает его данные и удаляет после теста"""
    response = requests.post(f"{BASE_URL}/auth/register", json=random_user)
    assert response.status_code == 200, "Ошибка регистрации пользователя"

    yield random_user

    # Логинимся, чтобы получить токен для удаления пользователя
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": random_user["email"],
        "password": random_user["password"]
    })
    assert login_response.status_code == 200, "Ошибка авторизации при удалении пользователя"
    token = login_response.json().get("accessToken")
    if token:
        requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})

@pytest.fixture
def auth_token(registered_user):
    """Возвращает токен авторизации для зарегистрированного пользователя"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200, "Ошибка авторизации пользователя"
    return response.json().get("accessToken")

@pytest.fixture
def ingredient_ids():
    """Получает список актуальных ID ингредиентов"""
    response = requests.get(f"{BASE_URL}/ingredients")
    assert response.status_code == 200, "Не удалось получить список ингредиентов"
    return [ingredient["_id"] for ingredient in response.json()["data"]]
