import json

import pytest

from cli import parse_schema
from notion_client.api import NotionClient
from notion_client.models import PropertyConfig, SchemaConfig, TaskProperty


@pytest.fixture
def notion_client():
    return NotionClient(api_key="fake_api_key")

def test_load_schema_alternative_format():
    schema_json = '''
    {
        "title": "Test Schema",
        "properties": [
            {"name": "Name", "type": "title"},
            {"name": "Status", "type": "select", "options": ["To Do", "Done"]}
        ]
    }
    '''
    schema_data = json.loads(schema_json)
    properties = parse_schema(schema_data)
    schema_config = SchemaConfig(title=schema_data['title'], properties=properties)
    assert schema_config.title == "Test Schema"
    assert "Name" in schema_config.properties
    assert schema_config.properties["Name"].property_type == "title"

def test_invalid_schema_format():
    schema_json = '''
    {
        "title": "Invalid Schema",
        "properties": {
            "Name": {"unknown_type": {}}
        }
    }
    '''
    schema_data = json.loads(schema_json)
    with pytest.raises(ValueError):
        parse_schema(schema_data)

def test_task_with_missing_property(notion_client, requests_mock):
    task_data = {
        "Task Name": "Sample Task",
        "Undefined Property": "Some Value"
    }
    schema_properties = {
        "Task Name": PropertyConfig(property_type="title"),
        # "Undefined Property" is not defined in the schema
    }
    with pytest.raises(ValueError):
        task_properties = {}
        for name, value in task_data.items():
            task_properties[name] = TaskProperty.from_value(name, value, schema_properties)

def test_database_creation_failure(notion_client, requests_mock):
    schema = SchemaConfig(title="Test DB", properties={})
    requests_mock.post(
        'https://api.notion.com/v1/databases',
        json={"message": "Validation error"},
        status_code=400
    )
    with pytest.raises(Exception):
        notion_client.create_database(parent_id="fake_page_id", schema=schema)
