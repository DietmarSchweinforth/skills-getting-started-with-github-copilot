"""
Pytest configuration and shared fixtures for FastAPI tests
"""

import pytest
from fastapi.testclient import TestClient
from copy import deepcopy
from src.app import app, activities


# Store the initial state of activities
INITIAL_ACTIVITIES = deepcopy(activities)


@pytest.fixture
def client(monkeypatch):
    """
    Fixture that provides a TestClient with fresh activity state for each test.
    
    Uses monkeypatch to reset the global activities dictionary to its initial
    state before each test, ensuring test isolation and preventing state pollution.
    """
    # Reset activities to initial state
    reset_activities = deepcopy(INITIAL_ACTIVITIES)
    monkeypatch.setattr("src.app.activities", reset_activities)
    
    # Return a TestClient instance
    return TestClient(app)
