import pytest


class TestStore:
    def test_get_inventory(self, api_client):
        response = api_client.get("store/inventory")
        assert response.status_code == 200

    def test_place_order(self, api_client, created_order):
        assert "id" in created_order

    def test_get_order(self, api_client, created_order):
        order_id = created_order["id"]
        response = api_client.get(f"store/order/{order_id}")
        assert response.status_code == 200

    def test_delete_order(self, api_client, created_order):
        order_id = created_order["id"]
        response = api_client.delete(f"store/order/{order_id}")
        assert response.status_code == 200
        get_response = api_client.get(f"store/order/{order_id}")
        assert get_response.status_code == 404

    def test_update_order_not_allowed(self, api_client, created_order):
        update_data = created_order.copy()
        update_data["status"] = "approved"
        response = api_client.put("store/order", json=update_data, headers={"Content-Type": "application/json"})
        assert response.status_code in [404, 405]

    @pytest.mark.parametrize("order_payload, expected_status", [
        ({
            "id": 1001,
            "petId": 2,
            "quantity": 2,
            "shipDate": "2025-03-11T00:00:00.000Z",
            "status": "placed",
            "complete": True
        }, 200),
        ({
            "id": 1002,
            "petId": 3,
            "quantity": 3,
            "shipDate": "2025-03-12T00:00:00.000Z",
            "status": "approved",
            "complete": False
        }, 200)
    ])
    def test_place_order_with_parameters(self, api_client, order_payload, expected_status):
        response = api_client.post("store/order", json=order_payload, headers={"Content-Type": "application/json"})
        assert response.status_code == expected_status
