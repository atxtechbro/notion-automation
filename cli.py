import click
import os
import json
from notion_client.api import NotionClient
from notion_client.config import ConfigManager
from notion_client.models import SchemaConfig, TaskConfig
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--schema', required=True, help='Path to the JSON schema file.')
@click.option('--tasks', required=True, help='Path to the JSON tasks file.')
def create_database(schema, tasks):
    # Get the Notion API key and page ID from environment variables
    notion_api_key = os.getenv('NOTION_API_KEY')
    notion_page_id = os.getenv('NOTION_PAGE_ID')

    if not notion_api_key or not notion_page_id:
        click.echo("Error: Please set the NOTION_API_KEY and NOTION_PAGE_ID in the .env file.")
        return

    # Load schema and tasks from the provided JSON files
    try:
        with open(schema, 'r') as schema_file:
            schema_data = json.load(schema_file)
        schema_config = SchemaConfig(**schema_data)

        with open(tasks, 'r') as tasks_file:
            tasks_data = json.load(tasks_file)
        tasks_config = [TaskConfig(**task) for task in tasks_data.get('tasks', [])]
    except FileNotFoundError as e:
        click.echo(f"Error: {e}")
        return
    except json.JSONDecodeError as e:
        click.echo(f"Error parsing JSON: {e}")
        return

    # Initialize Notion client
    notion_client = NotionClient(api_key=notion_api_key)

    # Create the database
    try:
        database_id = notion_client.create_database(parent_id=notion_page_id, schema=schema_config)
        click.echo(f"Database created successfully with ID: {database_id}")

        # Add tasks to the database
        for task in tasks_config:
            notion_client.create_task(database_id=database_id, task=task)
        click.echo("Tasks added successfully.")
    except Exception as e:
        click.echo(f"Error creating database or tasks: {e}")

if __name__ == "__main__":
    cli()
