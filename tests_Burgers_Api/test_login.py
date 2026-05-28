import allure
import requests
import pytest
from urls import Endpoints
from data import ERROR_MESSAGES

@allure.feature("Логин пользователя")
class TestUserLogin:

    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user_success(self, created_user):
        data = {
            "email": created_user["user"]["email"],
            "password": created_user["user"]["password"]
        }
        response = requests.post(Endpoints.LOGIN, json=data)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["success"] is True
        assert response_json["user"]["email"] == data["email"]
        assert "accessToken" in response_json
        assert "refreshToken" in response_json

    @allure.title("Вход с неверным email")
    def test_login_invalid_email(self, created_user):
        data = {
            "email": "wrong@email.ru",
            "password": created_user["user"]["password"]
        }
        response = requests.post(Endpoints.LOGIN, json=data)

        assert response.status_code == 401
        assert response.json()["message"] == ERROR_MESSAGES["invalid_credentials"]

    @allure.title("Вход с неверным паролем")
    def test_login_invalid_password(self, created_user):
        data = {
            "email": created_user["user"]["email"],
            "password": "wrong_password"
        }
        response = requests.post(Endpoints.LOGIN, json=data)

        assert response.status_code == 401
        assert response.json()["message"] == ERROR_MESSAGES["invalid_credentials"]

    @allure.title("Вход с неверным email и паролем")
    def test_login_invalid_both(self):
        data = {
            "email": "wrong@email.ru",
            "password": "wrong_password"
        }
        response = requests.post(Endpoints.LOGIN, json=data)

        assert response.status_code == 401
        assert response.json()["message"] == ERROR_MESSAGES["invalid_credentials"]