"""
Tests for Supabase Client module.
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from flask import Flask


@pytest.fixture
def app():
    """Create a Flask app for testing."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "test-secret-key"
    return app


@patch.dict(os.environ, {"SUPABASE_URL": "https://test.supabase.co", "SUPABASE_KEY": "test-key"})
def test_get_supabase_creates_client(app):
    """Test that get_supabase creates a client instance."""
    with app.app_context():
        from code.supabase_client import get_supabase

        client = get_supabase()
        assert client is not None


@patch.dict(os.environ, {"SUPABASE_URL": "", "SUPABASE_KEY": ""})
def test_get_supabase_with_empty_config(app):
    """Test that get_supabase handles empty configuration."""
    with app.app_context():
        from code.supabase_client import get_supabase

        # This should not raise an error, but may create an invalid client
        client = get_supabase()
        assert client is not None
