from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_without_name():
    response = client.get("/applicants", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_long_name():
    response = client.get("/applicants?name=authenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauth", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail" : "Name cannot be empty or longer than 200 characters"}

def test_read_nonexistent_empty_name():
    response = client.get("/applicants?name=", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail" : "Name cannot be empty or longer than 200 characters"}

def test_read_name_invalid_status():
    response = client.get("/applicants?name=abc&all_status=", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_name_wrong_status_type():
    response = client.get("/applicants?name=abc&all_status=3", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_by_address_without_contains():
    response = client.get("/applicants/address", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_by_address_contains_empty():
    response = client.get("/applicants/address?contains=", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail" : "address search string cannot be empty or longer than 200 characters"}

def test_read_by_address_long_contains():
    response = client.get("/applicants/address?contains=authenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauthenticsauth", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 400
    assert response.json() == {"detail" : "address search string cannot be empty or longer than 200 characters"}

def test_read_nearby_invalid_lat():
    response = client.get("/applicants/nearby?lat=abc&long=12", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

def test_read_nearby_lat_long_missing():
    response = client.get("/applicants/nearby", headers={"X-Token": "coneofsilence"})
    assert response.status_code == 422

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
