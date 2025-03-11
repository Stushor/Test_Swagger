import requests
import pytest
import random
from configparser import ConfigParser


def get_config():
    config = ConfigParser()
    config.read("config.ini")
    return config


@pytest.fixture(scope="session")
def api_config():
    config = get_config()
    return config["api"]["base_url"]


@pytest.fixture
def created_pet(api_config):
    new_pet = {
        "name": "Max",
        "category": {"id": 1, "name": "Cat"},
        "photoUrls": ["string"],
        "tags": [{"id": 1, "name": "tag2"}],
        "status": "available"
    }
    response = requests.post(
        f"{api_config}/pet",
        json=new_pet,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Max"
    assert data["status"] == "available"
    return data["id"]


@pytest.fixture
def created_user(api_config):
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
    response = requests.post(
        f"{api_config}/user",
        json=new_user,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    return new_user


@pytest.fixture
def created_order(api_config):
    order_data = {
        "id": random.randint(1, 100000),
        "petId": 1,
        "quantity": 1,
        "shipDate": "2025-03-11T00:00:00.000Z",
        "status": "placed",
        "complete": True
    }
    response = requests.post(
        f"{api_config}/store/order",
        json=order_data,
        headers={"Content-Type": "application/json"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "placed"
    return data


class TestPet:
    def test_get_pet_by_id(self, api_config, created_pet):
        response = requests.get(f"{api_config}/pet/{created_pet}")
        assert response.status_code == 200

    @pytest.mark.parametrize("pet_id, expected_status", [
        (None, 200),
        (999, 404)
    ])
    def test_pet_id_status(self, api_config, created_pet_id, pet_id, expected_status):
        if pet_id is None:
            pet_id = created_pet_id
        response = requests.get(f"{api_config}/pet/{pet_id}")
        assert response.status_code == expected_status

    def test_delete_pet(self, api_config, created_pet_id):
        response = requests.delete(f"{api_config}/pet/{created_pet}")
        assert response.status_code == 200

        get_response = requests.get(f"{api_config}/pet/{created_pet_id}")
        assert get_response.status_code == 404


class TestUser:
    def test_create_user(self, api_config, created_user):
        response = requests.get(f"{api_config}/user/{created_user['username']}")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == created_user["username"]

    def test_update_user(self, api_config, created_user):
        updated_data = created_user.copy()
        updated_data["firstName"] = "Updated"
        response = requests.put(
            f"{api_config}/user/{created_user['username']}",
            json=updated_data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 200

        get_response = requests.get(f"{api_config}/user/{created_user['username']}")
        assert get_response.status_code == 200
        data = get_response.json()
        assert data["firstName"] == "Updated"

    def test_delete_user(self, api_config, created_user):
        response = requests.delete(f"{api_config}/user/{created_user['username']}")
        assert response.status_code == 200

        get_response = requests.get(f"{api_config}/user/{created_user['username']}")
        assert get_response.status_code == 404


class TestStore:
    def test_get_inventory(self, api_config):
        response = requests.get(f"{api_config}/store/inventory")
        assert response.status_code == 200

    def test_place_order(self, api_config, created_order):
        assert "id" in created_order

    def test_get_order(self, api_config, created_order):
        order_id = created_order["id"]
        response = requests.get(f"{api_config}/store/order/{order_id}")
        assert response.status_code == 200

    def test_delete_order(self, api_config, created_order):
        order_id = created_order["id"]
        response = requests.delete(f"{api_config}/store/order/{order_id}")
        assert response.status_code == 200

        get_response = requests.get(f"{api_config}/store/order/{order_id}")
        assert get_response.status_code == 404

    def test_update_order_not_allowed(self, api_config, created_order):
        update_data = created_order.copy()
        update_data["status"] = "approved"
        response = requests.put(
            f"{api_config}/store/order",
            json=update_data,
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code in [404, 405]
