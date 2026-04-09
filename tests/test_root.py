"""
Tests for root endpoint
"""

import pytest


def test_root_endpoint_redirects_to_static(client):
    """
    Test that GET / redirects to /static/index.html.
    
    Arrange: Fresh app state
    Act: Send GET request to root endpoint with follow_redirects=False
    Assert: Response status is 307 (temporary redirect)
    """
    # Arrange
    expected_status_code = 307
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.status_code == expected_status_code


def test_root_endpoint_redirect_location(client):
    """
    Test that GET / redirects to the correct location.
    
    Arrange: Fresh app state
    Act: Send GET request to root endpoint with follow_redirects=False
    Assert: Location header points to /static/index.html
    """
    # Arrange
    expected_location = "/static/index.html"
    
    # Act
    response = client.get("/", follow_redirects=False)
    
    # Assert
    assert response.headers["location"] == expected_location


def test_root_endpoint_follow_redirect(client):
    """
    Test that following the redirect from GET / works.
    
    Arrange: Fresh app state
    Act: Send GET request to root endpoint with follow_redirects=True
    Assert: Final response status is 200
    """
    # Arrange
    # Act
    response = client.get("/", follow_redirects=True)
    
    # Assert
    assert response.status_code == 200
