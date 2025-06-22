import pytest
import requests
import allure
from conftest import BASE_URL


@allure.feature("Авторизация пользователя")
class TestUserLogin:
    @allure.title("Вход с валидными данными")
    def test_login_valid_user(self, registered_user):
        """Проверка успешной авторизации"""
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": registered_user["email"],
            "password": registered_user["password"]
        })

        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"
        assert "accessToken" in response.json(), "Нет токена доступа"
        assert "refreshToken" in response.json(), "Нет refresh-токена"

    @allure.title("Вход с неверными данными")
    def test_login_invalid_credentials(self, registered_user):
        """Проверка авторизации с неверным паролем"""
        response = requests.post(f"{BASE_URL}/auth/login", json={
            "email": registered_user["email"],
            "password": "неверный_пароль"
        })

        assert response.status_code == 401, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"

    @allure.title("Вход без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password"])
    def test_login_missing_field(self, registered_user, missing_field):
        """Проверка авторизации без обязательных полей"""
        login_data = {
            "email": registered_user["email"],
            "password": registered_user["password"]
        }
        del login_data[missing_field]  # Удаляем одно поле

        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)

        assert response.status_code == 401, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "email or password are incorrect", "Неверное сообщение об ошибке"