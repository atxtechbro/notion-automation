from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class PropertyOption(BaseModel):
    name: str
    color: Optional[str] = None

class PropertyConfig(BaseModel):
    property_type: str
    options: Optional[List[PropertyOption]] = None
    def to_notion_format(self):
        # Convert PropertyConfig to Notion API property format
        pass

class SchemaConfig(BaseModel):
    title: str
    properties: Dict[str, PropertyConfig]

    def to_notion_properties(self):
        notion_properties = {}
        for name, prop in self.properties.items():
            notion_properties[name] = prop.to_notion_format()
        return notion_properties

class TaskProperty(BaseModel):
    type: str
    value: Any

class TaskConfig(BaseModel):
    properties: Dict[str, TaskProperty]
