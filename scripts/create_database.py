import os
import json
import requests
import argparse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

NOTION_API_KEY = os.getenv('NOTION_API_KEY')
NOTION_PAGE_ID = os.getenv('NOTION_PAGE_ID')  # The ID of the Notion page where the database will be created

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

def load_database_config(config_name):
    config_path = f'config/database_configs/{config_name}.json'
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Template file '{config_path}' not found.")
    with open(config_path, 'r') as file:
        config = json.load(file)
    return config

def create_database(config):
    create_url = 'https://api.notion.com/v1/databases'

    data = {
        "parent": { "type": "page_id", "page_id": NOTION_PAGE_ID },
        "title": [
            {
                "type": "text",
                "text": {
                    "content": config["schema"]["title"]
                }
            }
        ],
        "properties": config["schema"]["properties"]
    }

    response = requests.post(create_url, headers=headers, json=data)

    if response.status_code == 200:
        database_id = response.json()["id"]
        print(f"Database created successfully with ID: {database_id}")
        return database_id
    else:
        print(f"Failed to create database: {response.text}")
        return None

def get_property_type(property_config):
    for property_type in ["title", "rich_text", "select", "date", "people", "url", "number", "multi_select"]:
        if property_type in property_config:
            return property_type
    return None

def validate_task_properties(task, schema_properties):
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

def create_task(database_id, task, schema_properties):
    validate_task_properties(task, schema_properties)

    create_url = 'https://api.notion.com/v1/pages'
    data = {
        "parent": {"database_id": database_id},
        "properties": task["properties"]
    }

    response = requests.post(create_url, headers=headers, json=data)

    if response.status_code == 200:
        task_name = task["properties"]["Name"]["title"][0]["text"]["content"]
        print(f"Task '{task_name}' created successfully.")
    else:
        print(f"Failed to create task: {response.text}")

def main(config_name):
    if NOTION_PAGE_ID is None or NOTION_PAGE_ID == '':
        print("Error: NOTION_PAGE_ID is not set or is empty. Please set it in the .env file.")
        return

    try:
        config = load_database_config(config_name)
        database_id = create_database(config)
        if database_id:
            tasks = config["tasks"]
            schema_properties = config["schema"]["properties"]
            
            for task in tasks:
                create_task(database_id, task, schema_properties)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"Validation Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create a Notion database using a specified template.")
    parser.add_argument('template', type=str, help="The name of the template to use (without .json extension).")
    
    args = parser.parse_args()
    main(args.template)
