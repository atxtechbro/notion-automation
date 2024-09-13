import os
import json
from typing import List
from .models import SchemaConfig, TaskConfig
import os
import json

class ConfigManager:
    def __init__(self, config_path='plugins'):
        self.config_path = config_path

    def load_schema(self, schema_name: str) -> SchemaConfig:
        file_path = os.path.join(self.config_path, f"{schema_name}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Schema file '{file_path}' not found.")
        with open(file_path, 'r') as file:
            data = json.load(file)
        return SchemaConfig(**data)

    def load_tasks(self, tasks_name: str) -> list:
        file_path = os.path.join(self.config_path, f"{tasks_name}.json")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Tasks file '{file_path}' not found.")
        with open(file_path, 'r') as file:
            data = json.load(file)
        tasks = [TaskConfig(**task) for task in data.get("tasks", [])]
        return tasks
