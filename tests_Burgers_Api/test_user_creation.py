import allure
import requests
import pytest
from helpers import generate_user_data
from data import ERROR_MESSAGES, REQUIRED_FIELDS
from urls import Endpoints

@pytest.fixture
def create_user_and_teardown():
    user_data = {}
    
    yield user_data  
    
    if "accessToken" in user_data:
        with allure.step("Пост-условие: Удаление созданного пользователя"):
            requests.delete(Endpoints.USER, headers={"Authorization": user_data["accessToken"]})

@allure.feature("Создание пользователя")
class TestUserCreation:

    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user_success(self, create_user_and_teardown):
        data = generate_user_data()
        with allure.step("Отправка POST-запроса на создание пользователя"):
            response = requests.post(Endpoints.REGISTER, json=data)

        assert response.status_code == 200
        response_json = response.json()
        assert response_json["success"] is True
        assert response_json["user"]["email"] == data["email"]
        assert response_json["user"]["name"] == data["name"]
        assert "accessToken" in response_json
        assert "refreshToken" in response_json

        if "accessToken" in  response_json:
            create_user_and_teardown["accessToken"] = response_json["accessToken"]

    @allure.title("Создание пользователя, который уже зарегистрирован")
    def test_create_existing_user_fails(self, created_user):
        data = created_user["user"]
        with allure.step("Отправка POST-запроса на создание пользователя"):
            response = requests.post(Endpoints.REGISTER, json=data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR_MESSAGES["user_exists"]

    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize('field_to_remove', REQUIRED_FIELDS)
    def test_create_user_missing_field_fails(self, field_to_remove):
        data = generate_user_data()
        del data[field_to_remove]
        with allure.step("Отправка POST-запроса на создание пользователя"):
            response = requests.post(Endpoints.REGISTER, json=data)

        assert response.status_code == 403
        assert response.json()["success"] is False
        assert response.json()["message"] == ERROR_MESSAGES["required_fields"]