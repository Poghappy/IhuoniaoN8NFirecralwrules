"""
Tests for Flask Session Storage module.
"""

import pytest
from flask import Flask, session
from code.flask_storage import FlaskSessionStorage


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret-key"
    return app


@pytest.fixture
def storage():
    """Create a FlaskSessionStorage instance."""
    return FlaskSessionStorage()


def test_get_nonexistent_key(app, storage):
    """Test getting a non-existent key returns None."""
    with app.test_request_context():
        assert storage.get("nonexistent") is None


def test_set_and_get(app, storage):
    """Test setting and getting a value."""
    with app.test_request_context():
        storage.set("test_key", "test_value")
        assert storage.get("test_key") == "test_value"


def test_remove_key(app, storage):
    """Test removing a key."""
    with app.test_request_context():
        storage.set("test_key", "test_value")
        storage.remove("test_key")
        assert storage.get("test_key") is None


def test_remove_nonexistent_key(app, storage):
    """Test removing a non-existent key doesn't raise an error."""
    with app.test_request_context():
        storage.remove("nonexistent")  # Should not raise an error
