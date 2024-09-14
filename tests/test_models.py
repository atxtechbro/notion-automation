import pytest
from pydantic import ValidationError

from notion_client.models import PropertyConfig, SchemaConfig, TaskProperty


def test_schema_config():
    data = {
        "title": "Test Schema",
        "properties": {
            "Name": PropertyConfig(property_type="title"),
            "Description": PropertyConfig(property_type="rich_text")
        }
    }
    schema = SchemaConfig(**data)
    assert schema.title == "Test Schema"
    assert "Name" in schema.properties
    assert schema.properties["Name"].property_type == "title"

def test_invalid_property_config():
    data = {
        "property_type": "invalid_type"
    }
    with pytest.raises(ValidationError) as exc_info:
        prop = PropertyConfig(**data)
    error_message = str(exc_info.value)
    assert "Unsupported property type: invalid_type" in error_message

def test_property_config_validator():
    with pytest.raises(ValidationError) as exc_info:
        PropertyConfig(property_type="invalid_type")
    error_message = str(exc_info.value)
    assert "Unsupported property type: invalid_type" in error_message

def test_task_property_validator():
    with pytest.raises(ValidationError) as exc_info:
        TaskProperty(type="unknown_type")
    error_message = str(exc_info.value)
    assert "Unsupported task property type: unknown_type" in error_message

def test_task_property_to_notion_format():
    task_prop = TaskProperty(type="title", value="Sample Task")
    notion_format = task_prop.to_notion_format()
    expected_format = {
        "title": [{
            "type": "text",
            "text": {"content": "Sample Task"}
        }]
    }
    assert notion_format == expected_format
