import pytest
import requests
import allure
from conftest import BASE_URL


@allure.feature("Создание заказа")
class TestOrderCreation:
    @allure.title("Создание заказа с ингредиентами (авторизованный)")
    def test_create_order_authorized(self, auth_token, ingredient_ids):
        """Проверка создания заказа с авторизацией"""
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": ingredient_ids[:2]}  # Берем 2 ингредиента

        response = requests.post(
            f"{BASE_URL}/orders",
            headers=headers,
            json=order_data
        )

        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"
        assert "name" in response.json(), "Нет названия бургера"
        assert "order" in response.json(), "Нет данных о заказе"

    @allure.title("Создание заказа с ингредиентами (неавторизованный)")
    def test_create_order_unauthorized(self, ingredient_ids):
        """Проверка создания заказа без авторизации"""
        order_data = {"ingredients": ingredient_ids[:2]}

        response = requests.post(f"{BASE_URL}/orders", json=order_data)

        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_no_ingredients(self, auth_token):
        """Проверка создания заказа без ингредиентов"""
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": []}

        response = requests.post(
            f"{BASE_URL}/orders",
            headers=headers,
            json=order_data
        )

        assert response.status_code == 400, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "Ingredient ids must be provided", "Неверное сообщение об ошибке"

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_ingredient(self, auth_token):
        """Проверка создания заказа с несуществующим ингредиентом"""
        headers = {"Authorization": auth_token}
        order_data = {"ingredients": ["неверный_хеш"]}

        response = requests.post(
            f"{BASE_URL}/orders",
            headers=headers,
            json=order_data
        )

        assert response.status_code == 500, "Неверный код ответа"