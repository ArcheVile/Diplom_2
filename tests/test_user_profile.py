import pytest
import requests
import allure
from conftest import BASE_URL


@allure.feature("Профиль пользователя")
class TestUserProfile:
    @allure.title("Обновление данных пользователя с авторизацией")
    @pytest.mark.parametrize("field,value", [
        ("name", "Новое Имя"),
        ("email", "new@email.com"),
        ("password", "newpassword123")
    ])
    def test_update_user_info_authorized(self, auth_token, field, value):
        """Проверка изменения данных пользователя"""
        headers = {"Authorization": auth_token}
        update_data = {field: value}

        response = requests.patch(
            f"{BASE_URL}/auth/user",
            headers=headers,
            json=update_data
        )

        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"
        assert response.json()["user"][field] == value, "Данные не обновились"

    @allure.title("Обновление данных без авторизации")
    def test_update_user_info_unauthorized(self):
        """Проверка изменения данных без токена"""
        response = requests.patch(
            f"{BASE_URL}/auth/user",
            json={"name": "Новое Имя"}
        )

        assert response.status_code == 401, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"

    @allure.title("Получение данных пользователя с авторизацией")
    def test_get_user_info_authorized(self, auth_token, registered_user):
        """Проверка получения данных пользователя"""
        headers = {"Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/auth/user", headers=headers)

        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"
        assert response.json()["user"]["email"] == registered_user["email"], "Неверный email"
        assert response.json()["user"]["name"] == registered_user["name"], "Неверное имя"

    @allure.title("Получение данных без авторизации")
    def test_get_user_info_unauthorized(self):
        """Проверка получения данных без токена"""
        response = requests.get(f"{BASE_URL}/auth/user")

        assert response.status_code == 401, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"