from dataclasses import dataclass
from typing import Dict, List, Optional

@dataclass
class PropertyOption:
    name: str
    color: Optional[str] = None
    
    def dict(self):
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "color": self.color
        }

@dataclass
class PropertyConfig:
    property_type: str
    options: Optional[List[PropertyOption]] = None

@dataclass
class SchemaConfig:
    title: str
    properties: Dict[str, PropertyConfig]

    def __post_init__(self):
        """Validate and convert properties if needed."""
        if not isinstance(self.properties, dict):
            raise ValueError("Properties must be a dictionary")
        
        # Convert any dict properties to PropertyConfig
        for name, prop in self.properties.items():
            if isinstance(prop, dict):
                self.properties[name] = PropertyConfig(**prop)
            elif not isinstance(prop, PropertyConfig):
                raise ValueError(f"Invalid property type for {name}")

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