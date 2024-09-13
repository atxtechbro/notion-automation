# File: tests/test_models.py
from notion_client.models import SchemaConfig, PropertyConfig

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
    try:
        prop = PropertyConfig(**data)
    except ValueError as e:
        assert str(e) == "Invalid property type: invalid_type"