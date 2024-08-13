# create_database.py
import argparse
from notion_utils.NotionUtils import load_database_config, create_database, create_task

def main(config_name):
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
