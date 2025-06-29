import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app, get_db
from database import Base

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_customer(db_session):
    response = client.post(
        "/customers/",
        json={"name": "Test Customer", "address": "123 Test St", "zip_code": "12345"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Customer"
    assert "id" in data

def test_read_customers(db_session):
    response = client.post(
        "/customers/",
        json={"name": "Test Customer", "address": "123 Test St", "zip_code": "12345"},
    )
    assert response.status_code == 200
    response = client.get("/customers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Test Customer"

def test_update_customer(db_session):
    response = client.post(
        "/customers/",
        json={"name": "Test Customer", "address": "123 Test St", "zip_code": "12345"},
    )
    customer_id = response.json()["id"]
    response = client.put(
        f"/customers/{customer_id}",
        json={"name": "Updated Customer", "address": "456 Updated St", "zip_code": "54321"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Customer"

def test_create_item(db_session):
    response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "description": "A test item",
            "manufacturer_name": "Test Inc.",
            "manufacturer_email": "test@example.com",
            "in_stock": 100,
            "reorder_quantity": 20,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

def test_create_order(db_session):
    customer_response = client.post(
        "/customers/",
        json={"name": "Test Customer", "address": "123 Test St", "zip_code": "12345"},
    )
    customer_id = customer_response.json()["id"]
    item_response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "description": "A test item",
            "manufacturer_name": "Test Inc.",
            "manufacturer_email": "test@example.com",
            "in_stock": 100,
            "reorder_quantity": 20,
        },
    )
    item_id = item_response.json()["id"]
    response = client.post(
        "/orders/",
        json={"item_id": item_id, "customer_id": customer_id, "order_quantity": 10},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["order_quantity"] == 10

def test_create_order_insufficient_stock(db_session):
    customer_response = client.post(
        "/customers/",
        json={"name": "Test Customer", "address": "123 Test St", "zip_code": "12345"},
    )
    customer_id = customer_response.json()["id"]
    item_response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "description": "A test item",
            "manufacturer_name": "Test Inc.",
            "manufacturer_email": "test@example.com",
            "in_stock": 5,
            "reorder_quantity": 20,
        },
    )
    item_id = item_response.json()["id"]
    response = client.post(
        "/orders/",
        json={"item_id": item_id, "customer_id": customer_id, "order_quantity": 10},
    )
    assert response.status_code == 400

def test_create_reorder_log(db_session):
    customer_response = client.post(
        "/customers/",
        json={"name": "Test Customer", "address": "123 Test St", "zip_code": "12345"},
    )
    customer_id = customer_response.json()["id"]
    item_response = client.post(
        "/items/",
        json={
            "name": "Test Item",
            "description": "A test item",
            "manufacturer_name": "Test Inc.",
            "manufacturer_email": "test@example.com",
            "in_stock": 25,
            "reorder_quantity": 20,
        },
    )
    item_id = item_response.json()["id"]
    client.post(
        "/orders/",
        json={"item_id": item_id, "customer_id": customer_id, "order_quantity": 10},
    )
    response = client.get("/reorder_logs/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["item_id"] == item_id