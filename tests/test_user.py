import pytest


class TestUser:
    def test_create_user(self, api_client, created_user):
        username = created_user["username"]
        response = api_client.get(f"user/{username}")
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == username

    def test_update_user(self, api_client, created_user):
        username = created_user["username"]
        updated_user = created_user.copy()
        updated_user["firstName"] = "Updated"
        response = api_client.put(f"user/{username}", json=updated_user, headers={"Content-Type": "application/json"})
        assert response.status_code == 200
        get_response = api_client.get(f"user/{username}")
        data = get_response.json()
        assert data["firstName"] == "Updated"

    def test_delete_user(self, api_client, created_user):
        username = created_user["username"]
        response = api_client.delete(f"user/{username}")
        assert response.status_code == 200
        get_response = api_client.get(f"user/{username}")
        assert get_response.status_code == 404

    @pytest.mark.parametrize("payload, expected_status", [
        ({
            "id": 1,
            "username": "param_user1",
            "firstName": "A",
            "lastName": "B",
            "email": "a@b.com",
            "password": "pass",
            "phone": "123456",
            "userStatus": 0
        }, 200),
        ({
            "id": 2,
            "username": "param_user2",
            "firstName": "C",
            "lastName": "D",
            "email": "c@d.com",
            "password": "pass",
            "phone": "654321",
            "userStatus": 1
        }, 200)
    ])
    def test_create_user_with_parameters(self, api_client, payload, expected_status):
        response = api_client.post("user", json=payload, headers={"Content-Type": "application/json"})
        assert response.status_code == expected_status
