import pytest
import json
from unittest.mock import Mock, patch
from notion_automation.notion_client import NotionClient
from notion_automation.models import SchemaConfig, PropertyConfig, PropertyOption

@pytest.fixture
def mock_notion_client():
    """Fixture for mocked Notion client."""
    with patch('notion_automation.notion_client.client.requests') as mock_requests:
        client = NotionClient("fake-token")
        # Mock successful response for database creation
        mock_requests.post.return_value.ok = True
        mock_requests.post.return_value.json.return_value = {"id": "test-db-id"}
        yield client, mock_requests

@pytest.fixture
def sample_schema():
    """Fixture for sample database schema."""
    return SchemaConfig(
        title="Test Database",
        properties={
            "Name": PropertyConfig(
                property_type="title"
            ),
            "Status": PropertyConfig(
                property_type="select",
                options=[
                    PropertyOption(name="Todo"),
                    PropertyOption(name="Done")
                ]
            )
        }
    )

def test_create_database(mock_notion_client, sample_schema):
    """Test database creation with schema."""
    client, mock_requests = mock_notion_client
    
    # Create database
    database_id = client.create_database("test-page-id", sample_schema)
    
    # Verify API call
    mock_requests.post.assert_called_once()
    call_args = mock_requests.post.call_args
    
    # Verify URL
    assert call_args[0][0] == "https://api.notion.com/v1/databases"
    
    # Verify payload
    payload = json.loads(json.dumps(call_args[1]["json"]))
    assert payload["parent"]["page_id"] == "test-page-id"
    assert payload["title"][0]["text"]["content"] == "Test Database"
    assert "Name" in payload["properties"]
    assert "Status" in payload["properties"]
    
    # Verify response
    assert database_id == "test-db-id"

def test_get_database_schema(mock_notion_client):
    """Test retrieving database schema."""
    client, mock_requests = mock_notion_client
    
    # Mock the get response
    mock_requests.get.return_value.ok = True
    mock_requests.get.return_value.json.return_value = {
        "title": [{"plain_text": "Test Database"}],
        "properties": {
            "Name": {
                "type": "title",
                "title": {}
            },
            "Status": {
                "type": "select",
                "select": {
                    "options": [
                        {"name": "Todo"},
                        {"name": "Done"}
                    ]
                }
            }
        }
    }
    
    # Get schema
    schema = client.get_database("test-db-id")
    
    # Verify API call
    mock_requests.get.assert_called_once_with(
        "https://api.notion.com/v1/databases/test-db-id",
        headers=client.headers
    )
    
    # Verify schema content
    assert schema["title"] == "Test Database"
    assert "Name" in schema["properties"]
    assert "Status" in schema["properties"]

def test_create_database_with_entries(mock_notion_client, sample_schema):
    """Test database creation with initial entries."""
    client, mock_requests = mock_notion_client
    
    # Mock responses for both database and page creation
    mock_requests.post.side_effect = [
        Mock(ok=True, json=lambda: {"id": "test-db-id"}),
        Mock(ok=True, json=lambda: {"id": "test-page-id"})
    ]
    
    # Create entries config
    entries = [
        {
            "Name": "Test Entry",
            "Status": "Todo"
        }
    ]
    
    # Create database with entries
    database_id = client.create_database("test-page-id", sample_schema)
    
    # Verify database creation
    assert database_id == "test-db-id"
    assert mock_requests.post.call_count >= 1
    
    # Add entries
    for entry in entries:
        client.create_entry(database_id, entry)
    
    # Verify entry creation calls
    assert mock_requests.post.call_count >= 2

def test_error_handling(mock_notion_client, sample_schema):
    """Test error handling in API calls."""
    client, mock_requests = mock_notion_client
    
    # Mock error response
    mock_requests.post.return_value.ok = False
    mock_requests.post.return_value.status_code = 400
    mock_requests.post.return_value.text = "Bad Request"
    
    # Verify error is raised
    with pytest.raises(Exception):
        client.create_database("test-page-id", sample_schema) 