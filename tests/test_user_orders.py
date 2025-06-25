import pytest
import requests
import allure
from config import BASE_URL



@allure.feature("Заказы пользователя")
class TestUserOrders:

    @allure.title("Получение заказов авторизованного пользователя")
    def test_get_user_orders_authorized(self, auth_token):
        with allure.step("Отправляем запрос с авторизацией"):
            headers = {"Authorization": auth_token}
            response = requests.get(f"{BASE_URL}/orders", headers=headers)

        with allure.step("Проверяем успешный ответ"):
            assert response.status_code == 200
            body = response.json()
            assert body["success"] is True
            assert "orders" in body

    @allure.title("Получение заказов неавторизованного пользователя")
    def test_get_user_orders_unauthorized(self):
        with allure.step("Отправляем запрос без авторизации"):
            response = requests.get(f"{BASE_URL}/orders")

        with allure.step("Проверяем ошибку"):
            assert response.status_code == 401
            body = response.json()
            assert body["success"] is False
            assert body["message"] == "You should be authorised"
