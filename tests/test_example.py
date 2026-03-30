import pytest

BASE = "/example"

VALID_PAYLOAD = {"name": "Jane Doe", "email": "jane@example.com", "age": 25}


# --- Auth guard ---

def test_list_requires_auth(client):
    res = client.get(BASE)
    assert res.status_code == 401


def test_get_requires_auth(client):
    res = client.get(f"{BASE}/1")
    assert res.status_code == 401


def test_create_requires_auth(client):
    res = client.post(BASE, json=VALID_PAYLOAD)
    assert res.status_code == 401


def test_delete_requires_auth(client):
    res = client.delete(f"{BASE}/1")
    assert res.status_code == 401


# --- POST /example ---

def test_create_success(client, auth_headers):
    res = client.post(BASE, json=VALID_PAYLOAD, headers=auth_headers)
    assert res.status_code == 201
    data = res.get_json()
    assert data["email"] == VALID_PAYLOAD["email"]
    assert data["name"] == VALID_PAYLOAD["name"]
    assert data["age"] == VALID_PAYLOAD["age"]
    assert "id" in data


def test_create_missing_field(client, auth_headers):
    res = client.post(BASE, json={"name": "No Email"}, headers=auth_headers)
    assert res.status_code == 400


def test_create_invalid_email(client, auth_headers):
    res = client.post(BASE, json={"name": "Bad", "email": "not-an-email", "age": 20}, headers=auth_headers)
    assert res.status_code == 400


def test_create_age_too_low(client, auth_headers):
    res = client.post(BASE, json={"name": "Young", "email": "y@example.com", "age": 10}, headers=auth_headers)
    assert res.status_code == 400


def test_create_name_too_short(client, auth_headers):
    res = client.post(BASE, json={"name": "X", "email": "x@example.com", "age": 20}, headers=auth_headers)
    assert res.status_code == 400


# --- GET /example ---

def test_list_returns_array(client, auth_headers):
    res = client.get(BASE, headers=auth_headers)
    assert res.status_code == 200
    assert isinstance(res.get_json(), list)


def test_list_contains_created_record(client, auth_headers):
    client.post(BASE, json={"name": "List Test", "email": "list@example.com", "age": 30}, headers=auth_headers)
    res = client.get(BASE, headers=auth_headers)
    emails = [u["email"] for u in res.get_json()]
    assert "list@example.com" in emails


# --- GET /example/<id> ---

def test_get_existing(client, auth_headers):
    created = client.post(BASE, json={"name": "Get Me", "email": "getme@example.com", "age": 22}, headers=auth_headers)
    user_id = created.get_json()["id"]
    res = client.get(f"{BASE}/{user_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["id"] == user_id


def test_get_not_found(client, auth_headers):
    res = client.get(f"{BASE}/999999", headers=auth_headers)
    assert res.status_code == 404


# --- DELETE /example/<id> ---

def test_delete_existing(client, auth_headers):
    created = client.post(BASE, json={"name": "Delete Me", "email": "deleteme@example.com", "age": 28}, headers=auth_headers)
    user_id = created.get_json()["id"]
    res = client.delete(f"{BASE}/{user_id}", headers=auth_headers)
    assert res.status_code == 200
    assert res.get_json()["message"] == "Deleted successfully"


def test_delete_confirms_gone(client, auth_headers):
    created = client.post(BASE, json={"name": "Gone Soon", "email": "gone@example.com", "age": 21}, headers=auth_headers)
    user_id = created.get_json()["id"]
    client.delete(f"{BASE}/{user_id}", headers=auth_headers)
    res = client.get(f"{BASE}/{user_id}", headers=auth_headers)
    assert res.status_code == 404


def test_delete_not_found(client, auth_headers):
    res = client.delete(f"{BASE}/999999", headers=auth_headers)
    assert res.status_code == 404
