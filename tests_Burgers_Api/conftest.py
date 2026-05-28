import pytest
import requests
import logging
from helpers import generate_user_data
from urls import Endpoints

@pytest.fixture
def user_data():
    return generate_user_data()

@pytest.fixture
def created_user(user_data):
    response = requests.post(Endpoints.REGISTER, json=user_data)
    
    if response.status_code != 200:
        pytest.fail(f"Не удалось создать пользователя. Статус: {response.status_code}")
    
    response_data = response.json()
    access_token = response_data.get("accessToken")
    
    yield {
        "user": user_data,
        "access_token": access_token,
        "refresh_token": response_data.get("refreshToken")
    }
    
    if access_token:
        headers = {"Authorization": access_token}
        delete_response = requests.delete(Endpoints.USER, headers=headers)
        if delete_response.status_code != 202:
            logging.warning(f"Не удалось удалить пользователя. Статус: {delete_response.status_code}")

@pytest.fixture
def ingredient_ids():
    response = requests.get(Endpoints.INGREDIENTS)
    
    if response.status_code != 200:
        pytest.fail(f"Не удалось получить ингредиенты. Статус: {response.status_code}")
    
    data = response.json()
    ids = [item["_id"] for item in data["data"]]
    return ids