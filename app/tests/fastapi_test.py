import unittest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestCalculator(unittest.TestCase):
    def setUp(self) -> None:
        self.test_data = {
            "cart_value": 790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2021-10-12T13:00:00Z",
        }

        self.test_invalid_data = {
            "cart_value": -790,
            "delivery_distance": 2235,
            "number_of_items": 4,
            "time": "2021-10-12T13:00:00Z",
        }

    def test_get(self) -> None:
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"Welcome to": "FastAPI Delivery Fee Calculator"}

    def test_post(self) -> None:
        response = client.post("/calculator/", json=self.test_data)
        assert response.status_code == 200
        assert response.json() == {"delivery_fee": 710}

    def test_error_handler(self) -> None:
        response = client.post("/calculator/", json=self.test_invalid_data)

        if response.status_code != 200:
            assert response.json() == {
                "msg": "You inserted invalid type of data on the fields."
            }
