import argparse
import json
import os
import sys

from dotenv import load_dotenv

from notion_client.api import NotionClient
from notion_client.logger import logger
from notion_client.models import PropertyConfig, PropertyOption, SchemaConfig, TaskConfig, TaskProperty

# Load environment variables from .env
load_dotenv()

def create_database(schema_path, tasks_path):
    """Creates a Notion database and adds tasks."""
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_page_id = os.getenv("NOTION_PAGE_ID")

    if not notion_api_key or not notion_page_id:
        print(
            "Error: Please set the NOTION_API_KEY and NOTION_PAGE_ID in the .env file."
        )
        sys.exit(1)

    try:
        with open(schema_path, "r") as schema_file:
            schema_data = json.load(schema_file)

        # Parse the schema
        properties = parse_schema(schema_data)

        schema_config = SchemaConfig(title=schema_data["title"], properties=properties)

        with open(tasks_path, "r") as tasks_file:
            tasks_data = json.load(tasks_file)

        tasks_config = []
        for task_data in tasks_data.get("tasks", []):
            task_properties = {}
            if "properties" in task_data:
                # Existing format
                for name, prop in task_data["properties"].items():
                    task_properties[name] = TaskProperty(**prop)
            else:
                # Simplified format
                for name, value in task_data.items():
                    task_properties[name] = TaskProperty.from_value(
                        name, value, properties
                    )
            tasks_config.append(TaskConfig(properties=task_properties))

    except FileNotFoundError as e:
        error_message = f"Error: {e}"
        logger.error(error_message)
        print(error_message)
        sys.exit(1)
    except json.JSONDecodeError as e:
        error_message = f"Error parsing JSON: {e}"
        logger.error(error_message)
        print(error_message)
        sys.exit(1)
    except Exception as e:
        error_message = f"Error processing schema or tasks: {e}"
        logger.error(error_message)
        print(error_message)
        sys.exit(1)

    try:
        notion_client = NotionClient(api_key=notion_api_key)
        database_id = notion_client.create_database(
            parent_id=notion_page_id, schema=schema_config
        )
        print(f"Database created successfully with ID: {database_id}")

        for task in tasks_config:
            notion_client.create_task(database_id=database_id, task=task)
        print("Tasks added successfully.")
    except Exception as e:
        error_message = f"Error creating database or tasks: {e}"
        logger.error(error_message)
        print(error_message)
        sys.exit(1)

def parse_schema(schema_data):
    """Parses the schema data into properties."""
    properties = {}

    if isinstance(schema_data["properties"], list):
        # Check if it's natural language descriptions
        if all(isinstance(p, str) for p in schema_data["properties"]):
            properties = parse_natural_language_properties(schema_data["properties"])
        else:
            # List of property dicts
            for prop in schema_data["properties"]:
                name = prop.get("name")
                property_type = prop.get("type")
                if not name or not property_type:
                    raise ValueError(f"Property definition is missing 'name' or 'type': {prop}")
                options = prop.get("options", [])
                property_options = [
                    PropertyOption(name=opt) if isinstance(opt, str) else PropertyOption(**opt)
                    for opt in options
                ]
                properties[name] = PropertyConfig(
                    property_type=property_type, options=property_options
                )
    elif isinstance(schema_data["properties"], dict):
        # Existing logic for dict format
        for name, prop in schema_data["properties"].items():
            if 'property_type' not in prop:
                raise ValueError(f"Property '{name}' is missing 'property_type'")
            property_type = prop["property_type"]
            options_data = prop.get("options", [])
            options = [PropertyOption(**option) for option in options_data]
            properties[name] = PropertyConfig(
                property_type=property_type, options=options
            )
    else:
        raise ValueError("Invalid schema format for 'properties' field.")

    return properties

def parse_natural_language_properties(property_descriptions):
    """Parses natural language property descriptions into PropertyConfig."""
    properties = {}
    for desc in property_descriptions:
        # Simple parsing logic
        try:
            name, rest = desc.split(":", 1)
        except ValueError:
            raise ValueError(f"Invalid property description format: '{desc}'")
        rest = rest.strip()
        options = None
        property_type = 'rich_text'  # Default type

        if "date" in rest.lower():
            property_type = "date"
        elif "status" in rest.lower() or "select" in rest.lower():
            property_type = "select"
            # Here, you could implement logic to extract options from the rest
            # For now, using default options
            options = [
                PropertyOption(name="To Do"),
                PropertyOption(name="In Progress"),
                PropertyOption(name="Done"),
            ]
        elif "number" in rest.lower():
            property_type = "number"
        elif "title" in rest.lower():
            property_type = "title"

        properties[name.strip()] = PropertyConfig(
            property_type=property_type, options=options
        )
    return properties

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Create a Notion database and add tasks."
    )
    parser.add_argument("--schema", required=True, help="Path to the JSON schema file.")
    parser.add_argument("--tasks", required=True, help="Path to the JSON tasks file.")

    # Parse the arguments
    args = parser.parse_args()

    # Call the create_database function with the provided arguments
    create_database(args.schema, args.tasks)
