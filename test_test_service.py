import pytest
from fastapi.testclient import TestClient
from test_service import app, items

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_items():
    """Clear items before each test."""
    items.clear()
    import test_service
    test_service.next_id = 1
    yield


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Test service is running"}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_create_and_get_item():
    new_item = {"name": "Test Laptop", "description": "High performance", "price": 999.99}
    create_res = client.post("/items", json=new_item)
    assert create_res.status_code == 201
    created_data = create_res.json()
    assert created_data["id"] == 1
    assert created_data["item"]["name"] == "Test Laptop"

    # Fetch the item
    get_res = client.get("/items/1")
    assert get_res.status_code == 200
    assert get_res.json()["name"] == "Test Laptop"
    assert get_res.json()["price"] == 999.99


def test_get_nonexistent_item():
    response = client.get("/items/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Item not found"


def test_update_item():
    # Create item
    client.post("/items", json={"name": "Book", "price": 15.0})

    # Update item
    update_res = client.put("/items/1", json={"name": "Book Updated", "description": "Second edition", "price": 20.0})
    assert update_res.status_code == 200
    assert update_res.json()["item"]["name"] == "Book Updated"
    assert update_res.json()["item"]["price"] == 20.0


def test_delete_item():
    client.post("/items", json={"name": "Item to Delete", "price": 5.0})
    del_res = client.delete("/items/1")
    assert del_res.status_code == 200
    assert del_res.json() == {"deleted": 1}

    # Verify deleted
    get_res = client.get("/items/1")
    assert get_res.status_code == 404
