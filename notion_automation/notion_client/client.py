import requests
import json
import logging
from notion_automation.logger import logger

logger = logging.getLogger(__name__)

class NotionClient:
    """Client for interacting with Notion API to manage databases and entries.
    
    Handles creation of databases with custom schemas and adding entries to those databases.
    Requires a valid Notion API key and page ID where databases will be created.
    
    Example usage:
        client = NotionClient(auth_token="your-notion-api-key")
        database_id = client.create_database(
            parent_id="your-page-id",
            schema=SchemaConfig(...)
        )
    """

    def __init__(self, auth_token):
        self.auth_token = auth_token
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {auth_token}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json"
        }

    def create_database(self, parent_id, schema):
        """Create a new Notion database with specified schema.
        
        Args:
            parent_id (str): ID of the parent page where database will be created
            schema (SchemaConfig): Database schema configuration
            
        Returns:
            str: ID of the created database
            
        Raises:
            requests.exceptions.HTTPError: If API request fails
        """
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
            raise Exception(f"Failed to create database: {response.text}")
        
        return response.json()["id"]

    def create_entry(self, database_id, entry):
        """Create a new entry in the database.
        
        Args:
            database_id (str): ID of the target database
            entry (dict or EntryConfig): Entry data
        """
        url = f"{self.base_url}/pages"
        
        # Handle both dict and EntryConfig inputs
        properties = entry.properties if hasattr(entry, 'properties') else entry
        
        payload = {
            "parent": {"database_id": database_id},
            "properties": self._format_entry_properties(properties)
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
        """Format a property configuration for Notion API.
        
        Handles different property types:
        - title: Database title field
        - rich_text: Multi-line text field
        - select: Single-select with options
        - date: Date field
        
        Args:
            prop (PropertyConfig): Property configuration
            
        Returns:
            dict: Formatted property for Notion API
        """
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

    def get_database(self, database_id):
        """Retrieve database schema from Notion.
        
        Args:
            database_id (str): ID of the database to retrieve
            
        Returns:
            dict: Database schema information
        """
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(url, headers=self.headers)
        
        if not response.ok:
            logger.error(f"Notion API error: {response.status_code}")
            logger.error(f"Response body: {response.text}")
            response.raise_for_status()
        
        return response.json()