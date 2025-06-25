import pytest
import requests
import allure
from config import BASE_URL



@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с ингредиентами (авторизованный)")
    def test_create_order_authorized(self, auth_token, ingredient_ids):
        with allure.step("Формируем заголовки и тело заказа"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": ingredient_ids[:2]}

        with allure.step("Отправляем запрос на создание заказа"):
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json=order_data)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "name" in body
            assert "order" in body

    @allure.title("Создание заказа с ингредиентами (неавторизованный)")
    def test_create_order_unauthorized(self, ingredient_ids):
        with allure.step("Формируем тело заказа"):
            order_data = {"ingredients": ingredient_ids[:2]}

        with allure.step("Отправляем запрос без авторизации"):
            response = requests.post(f"{BASE_URL}/orders", json=order_data)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, auth_token):
        with allure.step("Формируем заголовки и пустой список ингредиентов"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": []}

        with allure.step("Отправляем запрос"):
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json=order_data)

        with allure.step("Проверяем ошибку"):
            assert response.status_code == 400
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "Ingredient ids must be provided"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient(self, auth_token):
        with allure.step("Формируем заголовки и неверный ингредиент"):
            headers = {"Authorization": auth_token}
            order_data = {"ingredients": ["неверный_хеш"]}

        with allure.step("Отправляем запрос"):
            response = requests.post(f"{BASE_URL}/orders", headers=headers, json=order_data)

        with allure.step("Проверяем ошибку сервера"):
            assert response.status_code == 500
