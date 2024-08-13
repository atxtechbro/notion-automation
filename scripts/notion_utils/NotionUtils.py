# notion_utils.py
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

def load_database_config(config_name):
    """Load the database configuration from a JSON file."""
    config_path = f'config/database_configs/{config_name}.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Template file '{config_path}' not found.")
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def get_property_type(property_config):
    """Determine the type of a property based on its configuration."""
    for property_type in ["title", "rich_text", "select", "date", "people", "url", "number", "multi_select"]:
        if property_type in property_config:
            return property_type
    return None

def validate_task_properties(task, schema_properties):
    """Validate the properties of a task against the schema properties."""
    task_properties = task["properties"]
    for key, value in schema_properties.items():
        if key not in task_properties:
            raise ValueError(f"Task property '{key}' is missing.")
        expected_type = get_property_type(value)
        actual_type = get_property_type(task_properties[key])
        if expected_type != actual_type:
            raise ValueError(f"Task property '{key}' has incorrect type. Expected: {expected_type}, Got: {actual_type}")
        if expected_type == 'people' and not task_properties[key].get('people'):
            task_properties[key] = {"people": []}

def create_database(config):
    """Create a new Notion database using the provided configuration."""
    create_url = 'https://api.notion.com/v1/databases'
    data = {
        "parent": {"type": "page_id", "page_id": NOTION_PAGE_ID},
        "title": [{"type": "text", "text": {"content": config["schema"]["title"]}}],
        "properties": config["schema"]["properties"]
    }
    response = requests.post(create_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        database_id = response.json()["id"]
        print(f"Database created successfully with ID: {database_id}")
        return database_id
    else:
        print(f"Failed to create database: {response.text}")
        return None

def update_database(database_id, config):
    """Update an existing Notion database with the provided configuration."""
    update_url = f'https://api.notion.com/v1/databases/{database_id}'

    data = {}

    # Only include title if it's provided in the config
    if "schema" in config and "title" in config["schema"]:
        data["title"] = [{"type": "text", "text": {"content": config["schema"]["title"]}}]

    # Check if properties exist in the database schema before updating
    if "schema" in config and "properties" in config["schema"]:
        # Get the existing properties from the database
        existing_schema_response = requests.get(update_url, headers=HEADERS)
        if existing_schema_response.status_code != 200:
            raise ValueError(f"Failed to retrieve database schema: {existing_schema_response.text}")

        existing_properties = existing_schema_response.json().get("properties", {})

        # Filter properties to only include those that exist in the current schema
        data["properties"] = {k: v for k, v in config["schema"]["properties"].items() if k in existing_properties}
        
        # Log missing properties
        missing_properties = [k for k in config["schema"]["properties"] if k not in existing_properties]
        if missing_properties:
            print(f"Warning: The following properties are missing in the current database schema and won't be updated: {', '.join(missing_properties)}")
    else:
        raise ValueError("The configuration must include 'properties' under 'schema' to update the database.")

    if not data.get("properties"):
        raise ValueError("No valid properties found to update in the database schema.")

    response = requests.patch(update_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        print(f"Database updated successfully.")
    else:
        print(f"Failed to update database: {response.status_code} - {response.text}")

def create_task(database_id, task, schema_properties):
    """Create a new task in the specified Notion database."""
    validate_task_properties(task, schema_properties)
    create_url = 'https://api.notion.com/v1/pages'
    data = {
        "parent": {"database_id": database_id},
        "properties": task["properties"]
    }
    response = requests.post(create_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        task_name = task["properties"]["Name"]["title"][0]["text"]["content"]
        print(f"Task '{task_name}' created successfully.")
    else:
        print(f"Failed to create task: {response.text}")

def update_task(database_id, task, schema_properties):
    """Update an existing task in the specified Notion database."""
    validate_task_properties(task, schema_properties)
    update_url = f'https://api.notion.com/v1/pages/{task["id"]}'
    data = {"properties": task["properties"]}
    response = requests.patch(update_url, headers=HEADERS, json=data)
    if response.status_code == 200:
        task_name = task["properties"]["Name"]["title"][0]["text"]["content"]
        print(f"Task '{task_name}' updated successfully.")
    else:
        print(f"Failed to update task: {response.text}")
