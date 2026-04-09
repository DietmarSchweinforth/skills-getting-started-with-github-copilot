"""
Tests for activity retrieval endpoint
"""

import pytest


def test_get_activities_returns_all_activities(client):
    """
    Test that GET /activities returns all 9 activities.
    
    Arrange: Fresh app state with all activities initialized
    Act: Send GET request to /activities endpoint
    Assert: Response contains all 9 activities with status 200
    """
    # Arrange
    expected_activity_count = 9
    expected_activities = [
        "Chess Club", "Programming Class", "Gym Class", "Soccer",
        "Basketball", "Art Club", "Drama Club", "Math Club", "Debate Team"
    ]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    assert response.status_code == 200
    assert len(activities) == expected_activity_count
    assert set(activities.keys()) == set(expected_activities)


def test_get_activities_returns_activity_details(client):
    """
    Test that GET /activities returns complete activity details.
    
    Arrange: Fresh app state
    Act: Send GET request to /activities endpoint
    Assert: Each activity has required fields (description, schedule, max_participants, participants)
    """
    # Arrange
    required_fields = ["description", "schedule", "max_participants", "participants"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name, activity_data in activities.items():
        for field in required_fields:
            assert field in activity_data, f"Field '{field}' missing from {activity_name}"
        assert isinstance(activity_data["participants"], list)


def test_get_activities_chess_club_details(client):
    """
    Test that Chess Club activity has expected initial state.
    
    Arrange: Fresh app state
    Act: Send GET request to /activities endpoint
    Assert: Chess Club has correct description, schedule, max_participants, and 2 initial participants
    """
    # Arrange
    expected_description = "Learn strategies and compete in chess tournaments"
    expected_schedule = "Fridays, 3:30 PM - 5:00 PM"
    expected_max_participants = 12
    expected_participant_count = 2
    expected_participants = ["michael@mergington.edu", "daniel@mergington.edu"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    chess_club = activities["Chess Club"]
    
    # Assert
    assert chess_club["description"] == expected_description
    assert chess_club["schedule"] == expected_schedule
    assert chess_club["max_participants"] == expected_max_participants
    assert len(chess_club["participants"]) == expected_participant_count
    assert chess_club["participants"] == expected_participants


def test_get_activities_empty_activities_have_no_participants(client):
    """
    Test that activities with no participants return empty list.
    
    Arrange: Fresh app state
    Act: Send GET request to /activities endpoint
    Assert: Activities like Soccer and Basketball have empty participants list
    """
    # Arrange
    empty_activities = ["Soccer", "Basketball", "Art Club", "Drama Club", "Math Club", "Debate Team"]
    
    # Act
    response = client.get("/activities")
    activities = response.json()
    
    # Assert
    for activity_name in empty_activities:
        assert activities[activity_name]["participants"] == []
