import pytest


class TestPet:
    def test_get_pet_by_id(self, api_client, created_pet):
        pet_id = created_pet["id"]
        response = api_client.get(f"pet/{pet_id}")
        assert response.status_code == 200

    @pytest.mark.parametrize("pet_id, expected_status", [
        (None, 200),
        (999, 404)
    ])
    def test_pet_id_status(self, api_client, created_pet, pet_id, expected_status):
        if pet_id is None:
            pet_id = created_pet["id"]
        response = api_client.get(f"pet/{pet_id}")

        assert response.status_code == expected_status

    def test_update_pet(self, api_client, created_pet):
        pet_id = created_pet["id"]
        updated_pet = created_pet.copy()
        updated_pet["name"] = "UpdatedName"
        response = api_client.put("pet", json=updated_pet, headers={"Content-Type": "application/json"})
        assert response.status_code == 200

        get_response = api_client.get(f"pet/{pet_id}")
        data = get_response.json()
        assert data["name"] == "UpdatedName"

    def test_delete_pet(self, api_client, created_pet):
        pet_id = created_pet["id"]
        response = api_client.delete(f"pet/{pet_id}")
        assert response.status_code == 200

        get_response = api_client.get(f"pet/{pet_id}")
        assert get_response.status_code == 404
