from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_signup_registers_student_for_activity():
    activity_name = "Soccer Club"
    email = "new-student@example.com"

    # Arrange
    client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    activity = client.get("/activities").json()[activity_name]
    assert email in activity["participants"]


def test_duplicate_signup_returns_400():
    activity_name = "Chess Club"
    email = "duplicate-student@example.com"

    # Arrange
    client.delete(f"/activities/{activity_name}/signup?email={email}")
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_unregister_removes_student_from_activity():
    activity_name = "Chess Club"
    email = "remove-student@example.com"

    # Arrange
    client.delete(f"/activities/{activity_name}/signup?email={email}")
    client.post(f"/activities/{activity_name}/signup?email={email}")

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 200
    assert f"Removed {email}" in response.json()["message"]
    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_unknown_participant_returns_404():
    # Arrange
    activity_name = "Chess Club"
    email = "missing@example.com"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup?email={email}")

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up"
