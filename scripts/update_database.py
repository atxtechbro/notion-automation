# File: scripts/update_database.py
import argparse
import os
from notion_client.api import NotionClient
from notion_client.config import ConfigManager

def main(database_id, schema_name, tasks_name):
    config_manager = ConfigManager(config_path=args.config_path)
    schema = config_manager.load_schema(schema_name)
    tasks = config_manager.load_tasks(tasks_name)

    notion_api_key = os.getenv('NOTION_API_KEY')

    notion_client = NotionClient(api_key=notion_api_key)
    notion_client.update_database(database_id=database_id, schema=schema)

    for task in tasks:
        notion_client.create_task(database_id=database_id, task=task)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update an existing Notion database.")
    parser.add_argument('database_id', type=str, help="The ID of the database to update.")
    parser.add_argument('schema', type=str, help="Schema name without extension.")
    parser.add_argument('tasks', type=str, help="Tasks name without extension.")
    parser.add_argument('--config-path', type=str, default='plugins', help="Path to the configuration directory.")
    args = parser.parse_args()
    main(args.database_id, args.schema, args.tasks)
