import pytest
import requests
import allure
from conftest import BASE_URL


@allure.feature("Создание пользователя")
class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, random_user):
        """Проверка успешного создания нового пользователя"""
        response = requests.post(f"{BASE_URL}/auth/register", json=random_user)

        # Проверяем код ответа и тело ответа
        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"
        assert "accessToken" in response.json(), "Нет токена доступа"

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, registered_user):
        """Проверка попытки регистрации существующего пользователя"""
        response = requests.post(f"{BASE_URL}/auth/register", json=registered_user)

        assert response.status_code == 403, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "User already exists", "Неверное сообщение об ошибке"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, random_user, missing_field):
        """Проверка регистрации без обязательных полей"""
        user_data = random_user.copy()
        del user_data[missing_field]  # Удаляем одно поле

        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

        assert response.status_code == 403, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()[
                   "message"] == "Email, password and name are required fields", "Неверное сообщение об ошибке"