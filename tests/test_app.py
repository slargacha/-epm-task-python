import os
os.environ["SECRET_KEY"] = "testing-secret-key-only"

import pytest

from src.app import app


@pytest.fixture
def client():
    app.testing = True
    with app.test_client() as client:
        yield client


class TestAppIntegration:
    """Integration tests covering the Flask application endpoints."""

    def test_home_page(self, client):
        response = client.get("/")

        assert response.status_code == 200
        assert b"EPAM Python Task" in response.data
        assert b"Diccionario" in response.data

    def test_dictionary_lookup_success(self, client):
        response = client.get("/dictionary/apple")

        assert response.status_code == 200
        assert response.is_json
        payload = response.get_json()
        assert payload["word"] == "apple"
        assert payload["definition"] == "A fruit that grows on trees"

    def test_dictionary_lookup_not_found(self, client):
        response = client.get("/dictionary/nonexistent")

        assert response.status_code == 404
        payload = response.get_json()
        assert payload["error"] == "Can't find entry for nonexistent"

    def test_shop_total_endpoint(self, client):
        response = client.get("/shop/total?items=socks,shoes&tax=0.09")

        assert response.status_code == 200
        payload = response.get_json()
        assert payload["total"] == 70.85
        assert payload["items"] == ["socks", "shoes"]
        assert payload["tax"] == 0.09

    def test_shop_total_invalid_tax(self, client):
        response = client.get("/shop/total?items=socks&tax=abc")

        assert response.status_code == 400
        payload = response.get_json()
        assert "Invalid tax value" in payload["error"]

    def test_nth_letter_endpoint(self, client):
        response = client.get("/nth-letter?words=yoda,best,has")

        assert response.status_code == 200
        payload = response.get_json()
        assert payload["result"] == "yes"
        assert payload["words"] == ["yoda", "best", "has"]

    def test_nth_letter_missing_words(self, client):
        response = client.get("/nth-letter")

        assert response.status_code == 400
        payload = response.get_json()
        assert "required" in payload["error"]
