import os
import json
import argparse
from notion_client.api import NotionClient
from notion_client.models import SchemaConfig, TaskConfig
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def create_database(schema, tasks):
    """Creates a Notion database and adds tasks."""
    notion_api_key = os.getenv('NOTION_API_KEY')
    notion_page_id = os.getenv('NOTION_PAGE_ID')

    if not notion_api_key or not notion_page_id:
        print("Error: Please set the NOTION_API_KEY and NOTION_PAGE_ID in the .env file.")
        return

    try:
        with open(schema, 'r') as schema_file:
            schema_data = json.load(schema_file)
        schema_config = SchemaConfig(**schema_data)

        with open(tasks, 'r') as tasks_file:
            tasks_data = json.load(tasks_file)
        tasks_config = [TaskConfig(**task) for task in tasks_data.get('tasks', [])]
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return

    notion_client = NotionClient(api_key=notion_api_key)

    try:
        database_id = notion_client.create_database(parent_id=notion_page_id, schema=schema_config)
        print(f"Database created successfully with ID: {database_id}")

        for task in tasks_config:
            notion_client.create_task(database_id=database_id, task=task)
        print("Tasks added successfully.")
    except Exception as e:
        print(f"Error creating database or tasks: {e}")

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Create a Notion database and add tasks.")
    parser.add_argument('--schema', required=True, help='Path to the JSON schema file.')
    parser.add_argument('--tasks', required=True, help='Path to the JSON tasks file.')

    # Parse the arguments
    args = parser.parse_args()

    # Call the create_database function with the provided arguments
    create_database(args.schema, args.tasks)
