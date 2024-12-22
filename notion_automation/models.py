from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class PropertyOption:
    name: str
    color: Optional[str] = None

@dataclass
class PropertyConfig:
    property_type: str
    options: Optional[List[PropertyOption]] = None

@dataclass
class SchemaConfig:
    title: str
    properties: Dict[str, PropertyConfig]

@dataclass
class TaskProperty:
    value: str
    type: str = "text"

@dataclass
class TaskConfig:
    properties: Dict[str, TaskProperty]

@dataclass
class EntryProperty:
    value: str
    type: str = "text"

    @classmethod
    def from_value(cls, name: str, value: str, properties: Dict[str, PropertyConfig]):
        return cls(value=value, type=properties[name].property_type)

@dataclass
class EntryConfig:
    properties: Dict[str, EntryProperty] 