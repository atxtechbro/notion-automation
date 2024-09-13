# File: notion_client/models.py
from typing import Any, Dict, List, Optional

from pydantic import BaseModel


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
    value: Any

    def to_notion_format(self):
        if self.type == "title":
            return {
                "title": [{
                    "type": "text",
                    "text": {"content": self.value}
                }]
            }
        elif self.type == "select":
            return {"select": {"name": self.value}}
        elif self.type == "date":
            return {"date": {"start": self.value}}
        # Add other property types as needed
        else:
            raise ValueError(f"Unsupported task property type: {self.type}")

class TaskConfig(BaseModel):
    properties: Dict[str, TaskProperty]

    def to_notion_properties(self):
        return {name: prop.to_notion_format() for name, prop in self.properties.items()}
