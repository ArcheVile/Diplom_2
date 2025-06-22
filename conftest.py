import pytest
import requests
from faker import Faker

# Базовый URL API
BASE_URL = "https://stellarburgers.nomoreparties.site/api"
fake = Faker('ru_RU')  # Генератор тестовых данных


@pytest.fixture
def random_user():
    """Генерирует случайные данные пользователя"""
    return {
        "email": fake.email(),
        "password": fake.password(length=10),
        "name": fake.first_name()
    }


@pytest.fixture
def registered_user(random_user):
    """Регистрирует нового пользователя и возвращает его данные"""
    # Регистрация пользователя
    response = requests.post(f"{BASE_URL}/auth/register", json=random_user)
    assert response.status_code == 200, "Ошибка при регистрации пользователя"

    yield random_user  # Возвращаем данные для теста

    # Удаление пользователя после теста
    login_response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": random_user["email"],
        "password": random_user["password"]
    })
    token = login_response.json()["accessToken"]
    requests.delete(f"{BASE_URL}/auth/user", headers={"Authorization": token})


@pytest.fixture
def auth_token(registered_user):
    """Получает токен авторизации для зарегистрированного пользователя"""
    response = requests.post(f"{BASE_URL}/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    return response.json()["accessToken"]


@pytest.fixture
def ingredient_ids():
    """Получает актуальные ID ингредиентов из API"""
    response = requests.get(f"{BASE_URL}/ingredients")
    assert response.status_code == 200, "Не удалось получить список ингредиентов"
    return [ingredient["_id"] for ingredient in response.json()["data"]]