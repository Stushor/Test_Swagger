import pytest
import random
from configparser import ConfigParser
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from api_client import APIClient


def get_config():
    config = ConfigParser()
    config.read("config.ini")
    return config


@pytest.fixture(scope="session")
def api_client():
    config = get_config()
    base_url = config["api"]["base_url"]
    return APIClient(base_url)


@pytest.fixture
def created_pet(api_client):
    new_pet = {
        "name": "Max",
        "category": {"id": 1, "name": "Cat"},
        "photoUrls": ["string"],
        "tags": [{"id": 1, "name": "tag2"}],
        "status": "available"
    }
    response = api_client.post("pet", json=new_pet, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    return response.json()


@pytest.fixture
def created_user(api_client):
    random_suffix = random.randint(1000, 9999)
    username = f"testuser{random_suffix}"
    new_user = {
        "id": random.randint(1, 100000),
        "username": username,
        "firstName": "Test",
        "lastName": "User",
        "email": "test@example.com",
        "password": "password",
        "phone": "123456789",
        "userStatus": 1
    }
    response = api_client.post("user", json=new_user, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    return new_user


@pytest.fixture
def created_order(api_client):
    order_data = {
        "id": random.randint(1, 100000),
        "petId": 1,
        "quantity": 1,
        "shipDate": "2025-03-11T00:00:00.000Z",
        "status": "placed",
        "complete": True
    }
    response = api_client.post("store/order", json=order_data, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    return response.json()
