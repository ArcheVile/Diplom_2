import pytest
import requests
import allure
from config import BASE_URL



@allure.feature("Создание пользователя")
class TestUserCreation:
    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, random_user):
        with allure.step("Отправляем запрос на регистрацию нового пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=random_user)

        with allure.step("Проверяем код ответа и тело ответа"):
            assert response.status_code == 200, "Неверный код ответа"
            body = response.json()
            assert body["success"] is True, "Флаг успеха не True"
            assert "accessToken" in body, "Нет токена доступа"

    @allure.title("Создание уже зарегистрированного пользователя")
    def test_create_existing_user(self, registered_user):
        with allure.step("Пытаемся зарегистрировать уже существующего пользователя"):
            response = requests.post(f"{BASE_URL}/auth/register", json=registered_user)

        with allure.step("Проверяем, что получили ошибку"):
            assert response.status_code == 403, "Неверный код ответа"
            body = response.json()
            assert body["success"] is False, "Флаг успеха не False"
            assert body["message"] == "User already exists", "Неверное сообщение об ошибке"

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize("missing_field", ["email", "password", "name"])
    def test_create_user_missing_field(self, random_user, missing_field):
        with allure.step(f"Удаляем поле {missing_field} из данных пользователя"):
            user_data = random_user.copy()
            del user_data[missing_field]

        with allure.step("Пытаемся зарегистрировать пользователя с неполными данными"):
            response = requests.post(f"{BASE_URL}/auth/register", json=user_data)

        with allure.step("Проверяем ошибку в ответе"):
            assert response.status_code == 403, "Неверный код ответа"
            body = response.json()
            assert body["success"] is False, "Флаг успеха не False"
            assert body["message"] == "Email, password and name are required fields", "Неверное сообщение об ошибке"
