import pytest

from cli import parse_natural_language_properties
from notion_client.models import PropertyConfig


def test_parse_natural_language_properties():
    property_descriptions = [
        "Task Name: The name of the task.",
        "Due Date: The date by which the task should be completed.",
        "Status: The current status of the task (To Do, In Progress, Done)."
    ]
    properties = parse_natural_language_properties(property_descriptions)

    assert "Task Name" in properties
    assert properties["Task Name"].property_type == "rich_text"

    assert "Due Date" in properties
    assert properties["Due Date"].property_type == "date"

    assert "Status" in properties
    assert properties["Status"].property_type == "select"
    assert len(properties["Status"].options) == 3
