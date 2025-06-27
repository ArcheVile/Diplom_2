import pytest
import requests
import allure
from config import BASE_URL


@allure.feature("Профиль пользователя")
class TestUserProfile:

    @allure.title("Обновление имени и почты с авторизацией")
    @pytest.mark.parametrize("field,value", [
        ("name", "Новое Имя"),
        ("email", "new@email.com")
    ])
    def test_update_visible_fields_authorized(self, auth_token, field, value):
        with allure.step(f"Обновляем поле {field}"):
            headers = {"Authorization": auth_token}
            update_data = {field: value}
            response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json=update_data)

        with allure.step("Проверяем успешный ответ и наличие обновлённого значения в ответе"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["user"][field] == value

    @allure.title("Обновление пароля с авторизацией")
    def test_update_password_authorized(self, auth_token):
        with allure.step("Обновляем пароль"):
            headers = {"Authorization": auth_token}
            update_data = {"password": "newpassword123"}
            response = requests.patch(f"{BASE_URL}/auth/user", headers=headers, json=update_data)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            # Пароль в теле ответа не отображается, поэтому не проверяем поле user

    @allure.title("Обновление данных без авторизации")
    def test_update_user_info_unauthorized(self):
        with allure.step("Пытаемся обновить данные без токена"):
            response = requests.patch(f"{BASE_URL}/auth/user", json={"name": "Новое Имя"})

        with allure.step("Проверяем ошибку"):
            assert response.status_code == 401
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "You should be authorised"

    @allure.title("Получение данных пользователя с авторизацией")
    def test_get_user_info_authorized(self, auth_token, registered_user):
        with allure.step("Получаем данные пользователя"):
            headers = {"Authorization": auth_token}
            response = requests.get(f"{BASE_URL}/auth/user", headers=headers)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert body["user"]["email"] == registered_user["email"]
            assert body["user"]["name"] == registered_user["name"]

    @allure.title("Получение данных без авторизации")
    def test_get_user_info_unauthorized(self):
        with allure.step("Пытаемся получить данные без токена"):
            response = requests.get(f"{BASE_URL}/auth/user")

        with allure.step("Проверяем ошибку"):
            assert response.status_code == 401
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "You should be authorised"
