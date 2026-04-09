"""
Tests for activity signup and participant management endpoints
"""

import pytest


def test_signup_single_student_returns_success_message(client):
    """
    Test that signing up a new student returns a success message.
    
    Arrange: Fresh app state with Soccer activity (initially empty)
    Act: Send POST request to signup endpoint with email
    Assert: Response status is 200 and returns success message
    """
    # Arrange
    activity_name = "Soccer"
    email = "alex@mergington.edu"
    
    # Act
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"


def test_signup_adds_student_to_participants(client):
    """
    Test that signing up a student adds them to activity's participants list.
    
    Arrange: Fresh app state with Soccer activity (initially empty)
    Act: Send POST request to signup endpoint, then GET activities
    Assert: Student email appears in activity's participants list
    """
    # Arrange
    activity_name = "Soccer"
    email = "alex@mergington.edu"
    
    # Act
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    activities = activities_response.json()
    
    # Assert
    assert signup_response.status_code == 200
    assert email in activities[activity_name]["participants"]


def test_signup_multiple_students_same_activity(client):
    """
    Test that multiple students can sign up for the same activity.
    
    Arrange: Fresh app state with Soccer activity (initially empty)
    Act: Sign up two different students to the same activity
    Assert: Both students appear in participants list
    """
    # Arrange
    activity_name = "Soccer"
    email1 = "student1@mergington.edu"
    email2 = "student2@mergington.edu"
    
    # Act
    response1 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email1}
    )
    response2 = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email2}
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    
    # Assert
    assert response1.status_code == 200
    assert response2.status_code == 200
    assert email1 in participants
    assert email2 in participants
    assert len(participants) == 2


def test_remove_participant_returns_success_message(client):
    """
    Test that removing a participant returns a success message.
    
    Arrange: Fresh app state with Chess Club (has 2 initial participants)
    Act: Send DELETE request to remove one participant
    Assert: Response status is 200 and returns success message
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Initial participant
    
    # Act
    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"


def test_remove_participant_removes_from_list(client):
    """
    Test that removing a participant actually removes them from the list.
    
    Arrange: Fresh app state with Chess Club (has 2 initial participants)
    Act: Send DELETE request to remove one participant, then GET activities
    Assert: Participant is no longer in the activity's participants list
    """
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Initial participant
    
    # Act
    remove_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    activities_response = client.get("/activities")
    participants = activities_response.json()[activity_name]["participants"]
    
    # Assert
    assert remove_response.status_code == 200
    assert email not in participants
    assert len(participants) == 1  # Originally 2, now 1


def test_signup_then_remove_participant_workflow(client):
    """
    Test the complete workflow: signup a student, then remove them.
    
    Arrange: Fresh app state with Basketball activity (initially empty)
    Act: Sign up a student, then remove them
    Assert: Student added then removed from participants list
    """
    # Arrange
    activity_name = "Basketball"
    email = "newstudent@mergington.edu"
    
    # Act - Sign up
    signup_response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    # Verify signup
    activities_after_signup = client.get("/activities").json()
    assert email in activities_after_signup[activity_name]["participants"]
    
    # Act - Remove
    remove_response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": email}
    )
    
    # Assert - Verify removal
    activities_after_removal = client.get("/activities").json()
    assert remove_response.status_code == 200
    assert email not in activities_after_removal[activity_name]["participants"]
