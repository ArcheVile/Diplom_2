import pytest
import requests
import allure
from config import BASE_URL



@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, random_user):
        with allure.step("Отправляем запрос на регистрацию"):
            response = requests.post(f"{BASE_URL}/auth/register", json=random_user)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "accessToken" in body

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, registered_user):
        with allure.step("Пытаемся зарегистрировать существующего пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=registered_user)

        with allure.step("Проверяем ошибку"):
            assert response.status_code == 403
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "User already exists"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, random_user, missing_field):
        user_data = random_user.copy()
        del user_data[missing_field]

        with allure.step(f"Пытаемся зарегистрировать без поля {missing_field}"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

        with allure.step("Проверяем ошибку"):
            assert response.status_code == 403
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Email, password and name are required fields"
