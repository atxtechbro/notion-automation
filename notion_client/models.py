# File: notion_client/models.py
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, FieldValidationInfo, field_validator


class PropertyOption(BaseModel):
    name: str
    color: Optional[str] = None

    def to_notion_format(self):
        data = {'name': self.name}
        if self.color is not None:
            data['color'] = self.color
        return data

class PropertyConfig(BaseModel):
    property_type: str
    options: Optional[List[PropertyOption]] = None

    @field_validator('property_type')
    def validate_property_type(cls, v):
        allowed_types = ['title', 'select', 'date', 'rich_text', 'number']
        if v not in allowed_types:
            raise ValueError(f"Unsupported property type: {v}")
        return v

    def to_notion_format(self):
        notion_property = {}
        if self.property_type == "title":
            notion_property = {"title": {}}
        elif self.property_type == "select":
            notion_property = {
                "select": {
                    "options": [option.to_notion_format() for option in self.options]
                }
            }
        elif self.property_type == "date":
            notion_property = {"date": {}}
        # Add other property types as needed
        else:
            raise ValueError(f"Unsupported property type: {self.property_type}")
        return notion_property

class SchemaConfig(BaseModel):
    title: str
    properties: Dict[str, PropertyConfig]

    def to_notion_properties(self):
        return {name: prop.to_notion_format() for name, prop in self.properties.items()}

class TaskProperty(BaseModel):
    type: str
    value: Any = None

    @field_validator('type')
    def validate_property_type(cls, v):
        allowed_types = ['title', 'select', 'date', 'rich_text', 'number']
        if v not in allowed_types:
            raise ValueError(f"Unsupported task property type: {v}")
        return v

    @staticmethod
    def from_value(name: str, value: Any, schema_properties: Dict[str, PropertyConfig]):
        prop_config = schema_properties.get(name)
        if not prop_config:
            raise ValueError(f"Property '{name}' is not defined in the schema.")
        return TaskProperty(type=prop_config.property_type, value=value)

class TaskConfig(BaseModel):
    properties: Dict[str, TaskProperty]

    def to_notion_properties(self):
        return {name: prop.to_notion_format() for name, prop in self.properties.items()}
