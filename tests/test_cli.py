import json

import pytest

from cli import parse_natural_language_properties, parse_schema
from notion_client.models import PropertyConfig, PropertyOption


def test_parse_schema_natural_language():
    schema_data = {
        "title": "Test Schema",
        "properties": [
            "Task Name: The name of the task.",
            "Due Date: The date by which the task should be completed.",
            "Status: The current status of the task (To Do, In Progress, Done)."
        ]
    }
    properties = parse_schema(schema_data)
    assert "Task Name" in properties
    assert properties["Task Name"].property_type == "rich_text"
    assert "Due Date" in properties
    assert properties["Due Date"].property_type == "date"
    assert "Status" in properties
    assert properties["Status"].property_type == "select"

def test_parse_schema_invalid_format():
    schema_data = {
        "title": "Invalid Schema",
        "properties": "This should be a list or dict"
    }
    with pytest.raises(ValueError):
        parse_schema(schema_data)

def test_parse_natural_language_properties_invalid_description():
    property_descriptions = [
        "InvalidDescriptionWithoutColon"
    ]
    with pytest.raises(ValueError):
        parse_natural_language_properties(property_descriptions)
