import pytest

# Arrange-Act-Assert pattern is used for all tests

def test_root_redirect(client):
    # Arrange is handled by fixtures
    # Act
    response = client.get("/")
    # Assert
    assert response.status_code in (200, 307, 302)
    # Accepts 307/302 for redirect, 200 if TestClient follows redirect
    assert "text/html" in response.headers.get("content-type", "")


def test_get_activities(client):
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data, dict)


def test_signup_success(client):
    # Arrange
    email = "newstudent@mergington.edu"
    activity = "Chess Club"
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email in client.get("/activities").json()[activity]["participants"]


def test_signup_duplicate(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"  # already signed up
    # Act
    response = client.post(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_unknown_activity(client):
    # Act
    response = client.post("/activities/UnknownActivity/signup", params={"email": "someone@mergington.edu"})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]


def test_unregister_success(client):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 200
    assert email not in client.get("/activities").json()[activity]["participants"]


def test_unregister_not_found(client):
    # Arrange
    activity = "Chess Club"
    email = "notfound@mergington.edu"
    # Act
    response = client.delete(f"/activities/{activity}/signup", params={"email": email})
    # Assert
    assert response.status_code == 404
    assert "Participant not found" in response.json()["detail"]


def test_unregister_unknown_activity(client):
    # Act
    response = client.delete("/activities/UnknownActivity/signup", params={"email": "someone@mergington.edu"})
    # Assert
    assert response.status_code == 404
    assert "Activity not found" in response.json()["detail"]
