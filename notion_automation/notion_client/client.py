import requests
import json
import logging
from notion_automation.logger import logger

logger = logging.getLogger(__name__)

class NotionClient:
    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def create_database(self, parent_id, schema):
        url = f"{self.base_url}/databases"
        
        payload = {
            "parent": {"type": "page_id", "page_id": parent_id},
            "title": [{"type": "text", "text": {"content": schema.title}}],
            "properties": self._format_properties(schema.properties)
        }
        
        logger.debug(f"Creating database with payload: {json.dumps(payload, indent=2)}")
        
        response = requests.post(url, headers=self.headers, json=payload)
        
        if not response.ok:
            logger.error(f"Notion API error: {response.status_code}")
            logger.error(f"Response body: {response.text}")
        
        response.raise_for_status()
        return response.json()["id"]

    def create_entry(self, database_id, entry):
        url = f"{self.base_url}/pages"
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": self._format_entry_properties(entry.properties)
        }
        
        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()["id"]

    def _format_properties(self, properties):
        formatted = {}
        for name, prop in properties.items():
            formatted[name] = self._format_property(prop)
        return formatted

    def _format_property(self, prop):
        formatted = {"type": prop.property_type}
        
        if prop.property_type in ["select", "multi_select"] and prop.options:
            formatted[prop.property_type] = {
                "options": [{"name": opt.name} for opt in prop.options]
            }
        elif prop.property_type == "title":
            formatted["title"] = {}  # Title needs an empty config
        elif prop.property_type == "rich_text":
            formatted["rich_text"] = {}  # Rich text needs an empty config
        elif prop.property_type == "date":
            formatted["date"] = {}  # Date needs an empty config
        
        logger.debug(f"Formatted property: {json.dumps(formatted, indent=2)}")
        return formatted

    def _format_entry_properties(self, properties):
        formatted = {}
        for name, prop in properties.items():
            formatted[name] = self._format_entry_property(prop)
        return formatted

    def _format_entry_property(self, prop):
        if prop.type == "title":
            return {"title": [{"text": {"content": prop.value}}]}
        elif prop.type == "rich_text":
            return {"rich_text": [{"text": {"content": prop.value}}]}
        elif prop.type == "select":
            return {"select": {"name": prop.value}}
        elif prop.type == "date":
            return {"date": {"start": prop.value}}
        else:
            raise ValueError(f"Unsupported property type: {prop.type}") 