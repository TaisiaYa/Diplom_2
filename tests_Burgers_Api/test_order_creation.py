import allure
import requests
import pytest
from urls import Endpoints
from data import ERROR_MESSAGES

@allure.feature("Создание заказа")
class TestOrderCreation:

    @allure.title("Создание заказа с авторизацией и валидными ингредиентами")
    def test_create_order_auth_valid(self, created_user, ingredient_ids):
        headers = {"Authorization": created_user["access_token"]}
        payload = {"ingredients": ingredient_ids[:2]}
        response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["success"] is True
        assert "name" in response_json
        assert "order" in response_json
        assert "number" in response_json["order"]

    @allure.title("Создание заказа без авторизации")
    def test_create_order_no_auth(self, ingredient_ids):
        payload = {"ingredients": ingredient_ids[:2]}
        response = requests.post(Endpoints.ORDERS, json=payload)

        assert response.status_code == 200
        assert response.json()["success"] is True

    @allure.title("Создание заказа без ингредиентов")
    def test_create_order_empty_ingredients(self, created_user):
        headers = {"Authorization": created_user["access_token"]}
        payload = {"ingredients": []}
        response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)

        assert response.status_code == 400
        assert response.json()["message"] == ERROR_MESSAGES["no_ingredients"]

    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_invalid_hash(self, created_user):
        headers = {"Authorization": created_user["access_token"]}
        payload = {"ingredients": ["invalid_hash_123", "also_invalid"]}
        response = requests.post(Endpoints.ORDERS, json=payload, headers=headers)

        assert response.status_code == 500