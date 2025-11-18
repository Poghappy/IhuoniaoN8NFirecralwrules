"""
Tests for API Integration module.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from 代码模块.api_integration import HuoniaoAPIClient, PublishStatus


@pytest.fixture
def api_client():
    """Create a HuoniaoAPIClient instance for testing."""
    return HuoniaoAPIClient(base_url="https://test-api.com", api_key="test-key")


def test_client_initialization(api_client):
    """Test API client initialization."""
    assert api_client.base_url == "https://test-api.com"
    assert api_client.api_key == "test-key"


@patch("代码模块.api_integration.requests.post")
def test_publish_article_success(mock_post, api_client):
    """Test successful article publishing."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "status": "published"}
    mock_post.return_value = mock_response

    result = api_client.publish_article({"title": "Test Article", "content": "Test Content"})

    assert result["id"] == 1
    assert result["status"] == "published"


@patch("代码模块.api_integration.requests.post")
def test_publish_article_failure(mock_post, api_client):
    """Test article publishing failure."""
    mock_response = Mock()
    mock_response.status_code = 400
    mock_response.raise_for_status.side_effect = Exception("Bad Request")
    mock_post.return_value = mock_response

    with pytest.raises(Exception):
        api_client.publish_article({"title": "Test Article", "content": "Test Content"})
