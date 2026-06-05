import os
import sqlite3
import pytest
from secure_app import app, init_db, DATABASE

@pytest.fixture()
def client():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_db()

    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client

def test_valid_login(client):
    response = client.post("/login", json={
        "username": "admin",
        "password": "admin123"
    })

    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "success"
    assert body["user"] == "admin"
    assert body["role"] == "admin"

def test_invalid_credentials(client):
    response = client.post("/login", json={
        "username": "admin",
        "password": "wrong-password"
    })

    assert response.status_code == 401
    assert response.get_json()["status"] == "failed"

def test_sql_injection_prevention(client):
    injection_payloads = [
        {"username": "admin' OR '1'='1", "password": "anything"},
        {"username": "admin'--", "password": "anything"},
        {"username": "' OR 1=1--", "password": "anything"},
        {"username": "admin'; DROP TABLE users; --", "password": "anything"}
    ]

    for payload in injection_payloads:
        response = client.post("/login", json=payload)
        assert response.status_code in [400, 401]
        assert response.get_json()["status"] == "failed"

def test_input_validation_username_too_short(client):
    response = client.post("/login", json={
        "username": "ad",
        "password": "admin123"
    })

    assert response.status_code == 400

def test_input_validation_username_too_long(client):
    response = client.post("/login", json={
        "username": "a" * 51,
        "password": "admin123"
    })

    assert response.status_code == 400

def test_input_validation_special_characters(client):
    response = client.post("/login", json={
        "username": "admin' OR '1'='1",
        "password": "admin123"
    })

    assert response.status_code == 400

def test_password_hashing():
    if os.path.exists(DATABASE):
        os.remove(DATABASE)

    init_db()

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username='admin'")
    password_value = cursor.fetchone()[0]
    conn.close()

    assert password_value != "admin123"
    assert len(password_value) == 64
    assert all(character in "0123456789abcdef" for character in password_value)
