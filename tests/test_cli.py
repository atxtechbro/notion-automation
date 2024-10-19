import pytest

from cli import parse_natural_language_properties, parse_schema


def test_parse_schema_natural_language():
    schema_data = {
        "title": "Test Schema",
        "properties": [
            "Name: The name of the entry.",
            "Due Date: The date by which the entry should be completed.",
            "Category: The category of the entry (Type A, Type B, Type C)."
        ]
    }
    properties = parse_schema(schema_data)
    assert "Name" in properties
    assert properties["Name"].property_type == "rich_text"
    assert "Due Date" in properties
    assert properties["Due Date"].property_type == "date"
    assert "Category" in properties
    assert properties["Category"].property_type == "select"

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
