from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_unregister_participant_removes_email_from_activity():
    activity_name = "Chess Club"
    email = "student@example.com"

    client.delete(f"/activities/{activity_name}/signup?email={email}")

    register_response = client.post(f"/activities/{activity_name}/signup?email={email}")
    assert register_response.status_code == 200

    delete_response = client.delete(f"/activities/{activity_name}/signup?email={email}")
    assert delete_response.status_code == 200
    assert f"Removed {email}" in delete_response.json()["message"]

    activity = client.get("/activities").json()[activity_name]
    assert email not in activity["participants"]


def test_unregister_unknown_participant_returns_404():
    response = client.delete("/activities/Chess Club/signup?email=missing@example.com")
    assert response.status_code == 404
