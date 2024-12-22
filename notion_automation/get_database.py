import sys
import json
from notion_automation.notion_client import NotionClient
import os
from dotenv import load_dotenv

def get_database_schema(database_id):
    """Retrieve and format the schema of a Notion database."""
    load_dotenv()
    notion = NotionClient(auth_token=os.getenv("NOTION_API_KEY"))
    
    try:
        database = notion.get_database(database_id)
        
        # Extract and format the properties schema
        schema = {
            "title": database["title"],
            "properties": {}
        }
        
        for prop_name, prop_data in database["properties"].items():
            prop_type = prop_data["type"]
            prop_info = {
                "type": prop_type,
                "name": prop_name
            }
            
            # Add additional info for specific property types
            if prop_type == "select":
                prop_info["options"] = [
                    option["name"] for option in prop_data["select"]["options"]
                ]
            elif prop_type == "multi_select":
                prop_info["options"] = [
                    option["name"] for option in prop_data["multi_select"]["options"]
                ]
            
            schema["properties"][prop_name] = prop_info
        
        return schema

    except Exception as e:
        print(f"Error retrieving database: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    if len(sys.argv) != 2:
        print("Usage: python get_database.py <database_id>", file=sys.stderr)
        sys.exit(1)
    
    database_id = sys.argv[1]
    schema = get_database_schema(database_id)
    
    # Pretty print the schema
    print(json.dumps(schema, indent=2))

if __name__ == "__main__":
    main() 