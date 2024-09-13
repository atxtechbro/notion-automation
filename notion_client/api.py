import requests
from .models import SchemaConfig, TaskConfig

from .logger import logger

class NotionClient:
    # Existing code...

    def create_database(self, parent_id: str, schema: SchemaConfig) -> str:
        url = 'https://api.notion.com/v1/databases'
        data = {
            "parent": {"page_id": parent_id},
            "title": [{"type": "text", "text": {"content": schema.title}}],
            "properties": schema.to_notion_properties()
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            database_id = response.json()["id"]
            logger.info(f"Database '{schema.title}' created with ID: {database_id}")
            return database_id
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create database: {e.response.text}")
            raise

    def update_database(self, database_id: str, schema: SchemaConfig):
        url = f'https://api.notion.com/v1/databases/{database_id}'
        data = {
            "title": [{"type": "text", "text": {"content": schema.title}}],
            "properties": schema.to_notion_properties()
        }
        try:
            response = requests.patch(url, headers=self.headers, json=data)
            response.raise_for_status()
            logger.info(f"Database '{schema.title}' updated successfully.")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to update database: {e.response.text}")
            raise

    def create_task(self, database_id: str, task: TaskConfig):
        url = 'https://api.notion.com/v1/pages'
        data = {
            "parent": {"database_id": database_id},
            "properties": task.to_notion_properties()
        }
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            task_name = task.properties["Name"].value[0].text.content
            logger.info(f"Task '{task_name}' created in database '{database_id}'.")
        except requests.exceptions.HTTPError as e:
            logger.error(f"Failed to create task: {e.response.text}")
            raise
