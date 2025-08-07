from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_without_name():
    response = client.get("/applicants", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_long_name_204():
    response = client.get("/applicants?name=authenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauth", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"message" : "Name is either empty or too long"}

def test_read_nonexistent_empty_name():
    response = client.get("/applicants?name=", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"message" : "Name is either empty or too long"}

def test_read_by_address_without_contains():
    response = client.get("/applicants/address", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_by_address_contains_empty():
    response = client.get("/applicants/address?contains=", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"message" : "contains is empty"}

def test_read_by_address_long_contains():
    response = client.get("/applicants/address?contains=authenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauth", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200
    assert response.json() == {"message" : "contains is too long"}

def test_read_nearby():
    response = client.get("/applicants/nearby?lat=37.79&long=-122.40", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200

def test_read_nearby_all_status_true():
    response = client.get("/applicants/nearby?lat=37.79&long=-122.40&all_status=true", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200

def test_read_nearby_all_status_false():
    response = client.get("/applicants/nearby?lat=37.79&long=-122.40&all_status=false", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 200

def test_read_nearby_lat_missing():
    response = client.get("/applicants/nearby?long=-122.40", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_nearby_long_missing():
    response = client.get("/applicants/nearby?lat=37.79", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422
