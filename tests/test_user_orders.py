import pytest
import requests
import allure
from conftest import BASE_URL


@allure.feature("Заказы пользователя")
class TestUserOrders:
    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, auth_token):
        """Проверка получения списка заказов"""
        headers = {"Authorization": auth_token}
        response = requests.get(f"{BASE_URL}/orders", headers=headers)

        assert response.status_code == 200, "Неверный код ответа"
        assert response.json()["success"] is True, "Флаг успеха не True"
        assert "orders" in response.json(), "Нет списка заказов"

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_unauthorized(self):
        """Проверка получения заказов без авторизации"""
        response = requests.get(f"{BASE_URL}/orders")

        assert response.status_code == 401, "Неверный код ответа"
        assert response.json()["success"] is False, "Флаг успеха не False"
        assert response.json()["message"] == "You should be authorised", "Неверное сообщение об ошибке"