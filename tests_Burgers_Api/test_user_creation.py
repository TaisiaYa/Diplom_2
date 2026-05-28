import allure
import requests
import pytest
from helpers import generate_user_data
from data import ERROR_MESSAGES, REQUIRED_FIELDS
from urls import Endpoints

@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self):
        data = generate_user_data()
        response = requests.post(Endpoints.REGISTER, json=data)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["success"] is True
        assert response_json["user"]["email"] == data["email"]
        assert response_json["user"]["name"] == data["name"]
        assert "accessToken" in response_json
        assert "refreshToken" in response_json

        token = response_json["accessToken"]
        requests.delete(Endpoints.USER, headers={"Authorization": token})

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user_fails(self, created_user):
        data = created_user["user"]
        response = requests.post(Endpoints.REGISTER, json=data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR_MESSAGES["user_exists"]

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize('field_to_remove', REQUIRED_FIELDS)
    def test_create_user_missing_field_fails(self, field_to_remove):
        data = generate_user_data()
        del data[field_to_remove]
        response = requests.post(Endpoints.REGISTER, json=data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR_MESSAGES["required_fields"]