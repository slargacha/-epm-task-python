import os
os.environ["FLASK_SECRET_KEY"] = "testing-secret-key-only"

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

    def test_dictionary_add_route(self, client):
        word = "orange"
        definition = "A sweet citrus fruit"

        response = client.get(f"/dictionary/add?word={word}&definition={definition}")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["word"] == word
        assert payload["definition"] == definition
        assert "Palabra agregada" in payload["message"]

        lookup = client.get(f"/dictionary/{word}")
        assert lookup.status_code == 200
        lookup_payload = lookup.get_json()
        assert lookup_payload["definition"] == definition

    def test_shop_catalog_endpoint(self, client):
        response = client.get("/shop/catalog")
        assert response.status_code == 200
        payload = response.get_json()
        assert "catalog" in payload
        assert payload["catalog"]["socks"] == 5
        assert payload["catalog"]["shoes"] == 60

    def test_shop_add_endpoint(self, client):
        response = client.get("/shop/add?item=watch&price=55")
        assert response.status_code == 200
        payload = response.get_json()
        assert payload["item"] == "watch"
        assert payload["price"] == 55.0
        assert payload["catalog"]["watch"] == 55.0

        response_total = client.get("/shop/total?items=watch,socks&tax=0.10")
        assert response_total.status_code == 200
        payload_total = response_total.get_json()
        assert payload_total["total"] == 66.0

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

    def test_dictionary_add_missing_word(self, client):
        """Test dictionary add without word parameter."""
        response = client.get("/dictionary/add?definition=test")

        assert response.status_code == 400
        payload = response.get_json()
        assert "required" in payload["error"].lower() or "word" in payload["error"].lower()

    def test_dictionary_add_missing_definition(self, client):
        """Test dictionary add without definition parameter."""
        response = client.get("/dictionary/add?word=test")

        assert response.status_code == 400
        payload = response.get_json()
        assert "required" in payload["error"].lower() or "definition" in payload["error"].lower()

    def test_shop_add_missing_item(self, client):
        """Test shop add without item parameter."""
        response = client.get("/shop/add?price=55")

        assert response.status_code == 400
        payload = response.get_json()
        assert "required" in payload["error"].lower() or "item" in payload["error"].lower()

    def test_shop_add_missing_price(self, client):
        """Test shop add without price parameter."""
        response = client.get("/shop/add?item=watch")

        assert response.status_code == 400
        payload = response.get_json()
        assert "required" in payload["error"].lower() or "price" in payload["error"].lower()

    def test_shop_add_invalid_price(self, client):
        """Test shop add with invalid price (not a number)."""
        response = client.get("/shop/add?item=watch&price=notanumber")

        assert response.status_code == 400
        payload = response.get_json()
        assert "number" in payload["error"].lower()

    def test_shop_add_negative_price(self, client):
        """Test shop add with negative price."""
        response = client.get("/shop/add?item=watch&price=-10")

        assert response.status_code == 400
        payload = response.get_json()
        assert "greater than" in payload["error"].lower() or "zero" in payload["error"].lower()

    def test_shop_total_missing_items(self, client):
        """Test shop total without items parameter."""
        response = client.get("/shop/total?tax=0.09")

        assert response.status_code == 400
        payload = response.get_json()
        assert "items" in payload["error"].lower()

    def test_shop_total_empty_items(self, client):
        """Test shop total with empty items."""
        response = client.get("/shop/total?items=&tax=0.09")

        assert response.status_code == 400
        payload = response.get_json()
        assert "items" in payload["error"].lower()

    def test_nth_letter_empty_words(self, client):
        """Test nth letter with empty words parameter."""
        response = client.get("/nth-letter?words=")

        assert response.status_code == 400
        payload = response.get_json()
        assert "words" in payload["error"].lower() or "separated" in payload["error"].lower()
