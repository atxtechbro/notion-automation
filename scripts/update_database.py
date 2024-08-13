# update_database.py
import argparse
from notion_utils.NotionUtils import create_task, load_database_config, update_database

def main(database_id, config_name):
    try:
        config = load_database_config(config_name)
        update_database(database_id, config)
        tasks = config["tasks"]
        schema_properties = config["schema"]["properties"]
        for task in tasks:
            create_task(database_id, task, schema_properties)
    except FileNotFoundError as e:
        print(e)
    except ValueError as e:
        print(f"Validation Error: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Update an existing Notion database using a specified template.")
    parser.add_argument('database_id', type=str, help="The ID of the database to update.")
    parser.add_argument('template', type=str, help="The name of the template to use (without .json extension).")
    
    args = parser.parse_args()
    main(args.database_id, args.template)
