def test_get_activities_returns_activity_data(client):
    # Arrange
    expected_activity = "Chess Club"

    # Act
    response = client.get("/activities")
    data = response.json()

    # Assert
    assert response.status_code == 200
    assert expected_activity in data
    assert "description" in data[expected_activity]
    assert "participants" in data[expected_activity]
    assert isinstance(data[expected_activity]["participants"], list)


def test_signup_adds_new_participant(client):
    # Arrange
    activity_name = "Programming Class"
    new_email = "test.student@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={new_email}"
    )
    data = response.json()
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Signed up {new_email} for {activity_name}"
    assert new_email in activities[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{activity_name}/signup?email={existing_email}"
    )
    data = response.json()

    # Assert
    assert response.status_code == 400
    assert data["detail"] == "Student already signed up for this activity"


def test_remove_participant_success(client):
    # Arrange
    activity_name = "Chess Club"
    participant_email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )
    data = response.json()
    activities = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert data["message"] == f"Removed {participant_email} from {activity_name}"
    assert participant_email not in activities[activity_name]["participants"]


def test_remove_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    missing_email = "doesnotexist@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={missing_email}"
    )
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Participant not found"


def test_remove_missing_activity_returns_404(client):
    # Arrange
    activity_name = "Nonexistent Club"
    participant_email = "student@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants?email={participant_email}"
    )
    data = response.json()

    # Assert
    assert response.status_code == 404
    assert data["detail"] == "Activity not found"
