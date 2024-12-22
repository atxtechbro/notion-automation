import argparse
import json
import os
import re
import sys

from dotenv import load_dotenv

from notion_automation.notion_client import NotionClient
from notion_automation.logger import logger
from notion_automation.models import (
    PropertyConfig, 
    PropertyOption, 
    SchemaConfig, 
    TaskConfig, 
    TaskProperty,
    EntryConfig,
    EntryProperty
)
from notion_automation.get_database import get_database_schema

# Load environment variables from .env
load_dotenv()

def create_database(schema_path, entries_path=None, page_id=None):
    """Creates a Notion database and optionally adds entries."""
    notion_api_key = os.getenv("NOTION_API_KEY")
    notion_page_id_env = os.getenv("NOTION_PAGE_ID")

    # Determine the page ID to use
    notion_page_id = page_id if page_id else notion_page_id_env

    if not notion_api_key or not notion_page_id:
        print(
            "Error: Please set the NOTION_API_KEY and NOTION_PAGE_ID in the .env file or provide them as CLI arguments."
        )
        sys.exit(1)

    try:
        with open(schema_path, "r") as schema_file:
            schema_data = json.load(schema_file)

        # Parse the schema
        properties = parse_schema(schema_data)

        schema_config = SchemaConfig(title=schema_data["title"], properties=properties)

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
        error_message = f"Error processing schema: {e}"
        logger.error(error_message)
        print(error_message)
        sys.exit(1)

    entries_config = []

    if entries_path:
        try:
            with open(entries_path, "r") as entries_file:
                entries_data = json.load(entries_file)

            for entry in entries_data.get("entries", []):
                entry_properties = {}
                if "properties" in entry:
                    # Existing format
                    for name, prop in entry["properties"].items():
                        entry_properties[name] = EntryProperty(**prop)
                else:
                    # Simplified format
                    for name, value in entry.items():
                        entry_properties[name] = EntryProperty.from_value(
                            name, value, properties
                        )
                # Use keyword argument here
                entries_config.append(EntryConfig(properties=entry_properties))

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
            error_message = f"Error processing entries: {e}"
            logger.error(error_message)
            print(error_message)
            sys.exit(1)

    try:
        notion_client = NotionClient(notion_api_key)
        database_id = notion_client.create_database(
            parent_id=notion_page_id, schema=schema_config
        )
        print(f"Database created successfully with ID: {database_id}")

        if entries_config:
            for entry in entries_config:
                notion_client.create_entry(database_id, entry)
            print("Entries added successfully.")
    except Exception as e:
        error_message = f"Error creating database or entries: {e}"
        logger.error(error_message)
        print(error_message)
        sys.exit(1)

def parse_schema(schema_data):
    """Parse schema data into properties."""
    properties = {}
    
    if isinstance(schema_data["properties"], list):
        # Natural language or list format
        for prop in schema_data["properties"]:
            if isinstance(prop, str):
                # Natural language format
                name, desc = prop.split(":", 1)
                name = name.strip()
                desc = desc.strip()
                
                if "date" in desc.lower():
                    prop_type = "date"
                elif any(word in desc.lower() for word in ["category", "type", "status"]):
                    prop_type = "select"
                    # Extract options from parentheses
                    import re
                    options_match = re.search(r'\((.*?)\)', desc)
                    if options_match:
                        options = [
                            PropertyOption(name=opt.strip())
                            for opt in options_match.group(1).split(",")
                        ]
                    else:
                        options = None
                else:
                    prop_type = "rich_text"
                    options = None
                
                properties[name] = PropertyConfig(
                    property_type=prop_type,
                    options=options
                )
            else:
                # List of property objects format
                name = prop["name"]
                prop_type = prop["type"]
                options = [
                    PropertyOption(name=opt) if isinstance(opt, str) else PropertyOption(**opt)
                    for opt in prop.get("options", [])
                ]
                properties[name] = PropertyConfig(
                    property_type=prop_type,
                    options=options
                )
    else:
        # Dictionary format
        for name, config in schema_data["properties"].items():
            properties[name] = PropertyConfig(**config)
    
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

        # Check for keywords to determine property type
        if "date" in rest.lower():
            property_type = "date"
        elif any(keyword in rest.lower() for keyword in ["status", "select", "category"]):
            property_type = "select"
        
        # Detect options in parentheses
        match = re.search(r'\((.*?)\)', rest)
        if match:
            options_str = match.group(1)
            options = [PropertyOption(name=opt.strip()) for opt in options_str.split(",")]

        properties[name.strip()] = PropertyConfig(
            property_type=property_type, options=options
        )
    return properties

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Manage Notion databases"
    )
    
    # Create subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Create database command
    create_parser = subparsers.add_parser('create', help='Create a new database')
    create_parser.add_argument("--schema", required=True, help="Path to the JSON schema file.")
    create_parser.add_argument("--tasks", required=False, help="Path to the JSON tasks file.")
    
    # Get database schema command
    get_parser = subparsers.add_parser('get-schema', help='Get schema of existing database')
    get_parser.add_argument("--id", required=True, help="ID of the database to retrieve")
    get_parser.add_argument("--output", help="Optional file path to save the schema")
    
    args = parser.parse_args()
    
    if args.command == 'create':
        create_database(args.schema, args.tasks)
    elif args.command == 'get-schema':
        schema = get_database_schema(args.id)
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(schema, f, indent=2)
            print(f"Schema saved to {args.output}")
        else:
            print(json.dumps(schema, indent=2))
