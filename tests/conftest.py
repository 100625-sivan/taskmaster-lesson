"""
Test configuration - makes the Flask app available to all test files.
"""

import sys
import os

# Add the app directory to the Python path so we can import app.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "app"))

from app import app as flask_app  # noqa: E402


import pytest  # noqa: E402


@pytest.fixture
def app():
    """Create the Flask app for testing."""
    flask_app.config["TESTING"] = True
    yield flask_app


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()
